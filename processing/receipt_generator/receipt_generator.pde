import processing.video.*;
import oscP5.*;
import netP5.*;
import java.util.Arrays;
import javax.print.*;
import javax.print.attribute.*;
import javax.print.attribute.standard.*;
import java.io.*;

PImage bg; 
PImage defaultImage;
Capture cam; 
PFont font;
OscP5 oscP5; 

String[] categories = {
  "Religion & Beliefs",
  "Loved Ones",
  "Travel & Culture",
  "Achievements & Triumph",
  "Aspirations",
  "Cues of Reassurance",
  "Hobbies & Interests",
  "Practicality & Utility",
};

float[] defaultValues = {0, 0, 0, 0, 0, 0, 0, 0}; 
float[] values = defaultValues.clone(); 

PImage[] stamps = new PImage[1];
float textStartY = 780; 
float textSpacing = 50; 
float datePosX = 170; 
float datePosY = 100; 
float camX; 
float camY = 320; 
float camWidth; 
float camHeight; 

int count = 0; 
String sentimentVal = ""; 
boolean needsUpdate = true;  // Flag to control redrawing

void setup() {
    size(359, 1538);
    bg = loadImage("TicketBG.jpg"); 
    defaultImage = loadImage("defaultImage.jpg"); 
    defaultImage.filter(GRAY);
    
    font = createFont("TimesNewRomanB.ttf", 30); 
    textFont(font);
    textAlign(CENTER, CENTER); 

    for (int i = 0; i < stamps.length; i++) {
        stamps[i] = loadImage("stamp_" + i + ".png");
        if (stamps[i] == null) {
            println("Error loading image: stamp_" + i + ".png");
        }
    }

    String[] cameras = Capture.list();
    if (cameras.length == 0) {
        println("No camera detected! Using default image.");
        cam = null;
    } else {
        cam = new Capture(this, cameras[0]); 
        cam.start();
    }
    
    camWidth = width * 2 / 3; 
    camHeight = camWidth * (float) defaultImage.height / defaultImage.width; 
    camX = (width - camWidth) / 2; 

    oscP5 = new OscP5(this, 1334);  // Listening on port 1334
}

void draw() {
    if (needsUpdate) {  // Only redraw if there’s an update
        image(bg, 0, 0);

        if (cam != null && cam.available()) {
            cam.read(); 
            cam.filter(GRAY); 
            drawHalftone(cam, camX, camY, camWidth, camHeight); 
        } else {
            image(defaultImage, camX, camY, camWidth, camHeight);
        }

        fill(0); 

        textSize(23);
        int categoryX = 30; 
        int valueX = width - 30;

        for (int i = 0; i < categories.length; i++) {
            textAlign(LEFT, CENTER);
            text(categories[i], categoryX, textStartY + i * textSpacing);

            textAlign(RIGHT, CENTER);
            text(String.format("%d%%", (int)values[i]), valueX, textStartY + i * textSpacing);
        }

        sentimentVal = getTopCategoriesAbbr(3);

        textSize(20);
        textAlign(CENTER, CENTER);
        String currentDate = year() + nf(month(), 2) + nf(day(), 2);
        String customText = String.format("(00)%d%s%s", count, currentDate, sentimentVal);
        text(customText, width / 2, 1480);

        text(currentDate, datePosX, datePosY);

        int highestIndex = getHighestValueIndex();
        highestIndex = min(highestIndex, stamps.length - 1);

        PImage stampToDisplay = stamps[highestIndex];

        if (stampToDisplay != null) {
            float scaleFactor = 0.4; 
            float newWidth = stampToDisplay.width * scaleFactor;
            float newHeight = stampToDisplay.height * scaleFactor;

            pushMatrix(); 
            translate(2, 400);
            rotate(radians(30));
            image(stampToDisplay, 0, 0, newWidth, newHeight); 
            popMatrix();
        }

        needsUpdate = false;  // Reset the flag after drawing
    }
}

void oscEvent(OscMessage msg) {
    if (msg.checkAddrPattern("/update_data") && msg.checkTypetag("s")) {
        String data = msg.get(0).stringValue();
        println("Received OSC Data: " + data); // Debug line to check data

        updateValues(data);
        delay(1000);
        saveAndPrintImage();
    }
}

void updateValues(String data) {
    String[] items = data.split(",");
    for (int i = 0; i < items.length && i < values.length; i++) {
        String[] parts = items[i].split(":");
        if (parts.length == 2) {
            float value = Float.parseFloat(parts[1].trim()) * 100;
            values[i] = value; // Directly assign to values array in the received order
        }
    }
    println("Updated values: " + Arrays.toString(values)); // Debug line to check values

    needsUpdate = true;  // Set flag to trigger redraw
}



String getTopCategoriesAbbr(int n) {
    Integer[] indices = new Integer[values.length];
    for (int i = 0; i < values.length; i++) {
        indices[i] = i;
    }

    Arrays.sort(indices, (a, b) -> Float.compare(values[b], values[a]));

    StringBuilder result = new StringBuilder();
    for (int i = 0; i < n && i < indices.length; i++) {
        int index = indices[i];
        String categoryAbbr = categories[index].substring(0, 3).toUpperCase();
        result.append(categoryAbbr);
    }

    return result.toString();
}

void drawHalftone(PImage img, float x, float y, float w, float h) {
    img.loadPixels();
    for (int yOffset = 0; yOffset < img.height; yOffset += 2) {
        for (int xOffset = 0; xOffset < img.width; xOffset += 2) {
            int index = xOffset + yOffset * img.width;
            int c = img.pixels[index];
            float bright = brightness(c);
            float dotSize = map(bright, 0, 255, 2, 10);
            noStroke();
            fill(c);
            ellipse(x + xOffset * (w / img.width), y + yOffset * (h / img.height), dotSize, dotSize);
        }
    }
}

int getHighestValueIndex() {
    int highestIndex = 0;
    for (int i = 1; i < values.length; i++) {
        if (values[i] > values[highestIndex]) {
            highestIndex = i;
        }
    }
    return highestIndex;
}

void saveAndPrintImage() {
    String fileName = "output_" + year() + nf(month(), 2) + nf(day(), 2) + "_" + count + ".jpg"; // Save as JPEG
    save(fileName); 
    
    //try {
    //    FileInputStream fis = new FileInputStream(fileName);
    //    DocFlavor flavor = DocFlavor.INPUT_STREAM.JPEG; // Use JPEG format
    //    Doc myDoc = new SimpleDoc(fis, flavor, null);

    //    PrintRequestAttributeSet aset = new HashPrintRequestAttributeSet();
    //    aset.add(new Copies(1)); 
    //    aset.add(PrintQuality.HIGH);

    //    // Find the printer named "POS-58"
    //    PrintService[] services = PrintServiceLookup.lookupPrintServices(flavor, aset);
    //    PrintService posPrinter = null;

    //    for (PrintService service : services) {
    //        if (service.getName().equals("POS-58")) {
    //            posPrinter = service;
    //            break;
    //        }
    //    }

    //    if (posPrinter != null) {
    //        DocPrintJob job = posPrinter.createPrintJob();
    //        job.print(myDoc, aset);
    //        println("Image saved as " + fileName + " and sent to POS-58 printer.");
    //    } else {
    //        println("Printer 'POS-58' not found.");
    //    }
        
    //    fis.close();
    //} catch (Exception e) {
    //    e.printStackTrace();
    //    println("Failed to print image.");
    //}
}
