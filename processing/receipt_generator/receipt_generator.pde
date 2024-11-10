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
    "Loved ones", 
    "Travel & Culture", 
    "Achievement", 
    "Aspiration", 
    "Hobbies", 
    "Relief & Reassurance", 
    "Religion & Belief",
    "Practicality" 
};

float[] defaultPercentages = {77, 10, 6, 3.5, 2.5, 0.9, 0.1, 0}; 
float[] percentages = defaultPercentages.clone(); 

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
boolean buttonPressed = false; 

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

    oscP5 = new OscP5(this, 12000);

    // List available printers to confirm the printer name
    //listPrinters();
}

void draw() {
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
    int categoryX = 30; // Left position for category text, moved further left
    int percentageX = width - 30; // Right position for percentage values, moved further right
    
    for (int i = 0; i < categories.length; i++) {
        // Align category text to the left
        textAlign(LEFT, CENTER);
        text(categories[i], categoryX, textStartY + i * textSpacing);

        // Align percentage values to the right
        textAlign(RIGHT, CENTER);
        text(String.format("%.2f%%", percentages[i]), percentageX, textStartY + i * textSpacing);
    }

    sentimentVal = getTopCategoriesAbbr(3);

    textSize(20);
    textAlign(CENTER, CENTER);
    String currentDate = year() + nf(month(), 2) + nf(day(), 2);
    String customText = String.format("(00)%d%s%s", count, currentDate, sentimentVal);
    text(customText, width / 2, 1480);

    text(currentDate, datePosX, datePosY);

    drawButton();
    
    int highestIndex = getHighestPercentageIndex();
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
}



void drawButton() {
    float buttonX = 50;
    float buttonY = 50;
    float buttonDiameter = 40;

    fill(buttonPressed ? color(100) : color(150)); 
    ellipse(buttonX, buttonY, buttonDiameter, buttonDiameter); 
    fill(0); 
    textSize(12);
    text("Add", buttonX, buttonY); 
}

void mousePressed() {
    float buttonX = 50;
    float buttonY = 50;
    float buttonDiameter = 40;

    if (dist(mouseX, mouseY, buttonX, buttonY) < buttonDiameter / 2) {
        buttonPressed = true; 
        count++; 
        saveAndPrintImage();
    }
}

void mouseReleased() {
    buttonPressed = false; 
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

void listPrinters() {
    PrintService[] services = PrintServiceLookup.lookupPrintServices(null, null);
    for (PrintService service : services) {
        println("Available printer: " + service.getName());
    }
}

String getTopCategoriesAbbr(int n) {
    Integer[] indices = new Integer[percentages.length];
    for (int i = 0; i < percentages.length; i++) {
        indices[i] = i;
    }

    Arrays.sort(indices, (a, b) -> Float.compare(percentages[b], percentages[a]));

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

void oscEvent(OscMessage msg) {
    for (int i = 0; i < categories.length; i++) {
        if (msg.checkAddrPattern("/" + categories[i].replace(" ", "_").toLowerCase()) && msg.checkTypetag("f")) {
            percentages[i] = msg.get(0).floatValue(); 
        }
    }
}

int getHighestPercentageIndex() {
    int highestIndex = 0;
    for (int i = 1; i < percentages.length; i++) {
        if (percentages[i] > percentages[highestIndex]) {
            highestIndex = i;
        }
    }
    return highestIndex;
}
