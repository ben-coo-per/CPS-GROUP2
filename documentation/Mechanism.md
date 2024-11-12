# Ripple Mechanism
The ripple mechanism is the central interactive and aesthetic element of our Sentimental Aura Robot. When a sentimental object is placed on the podium, sensors detect its presence, activating a motor at the base that drives a series of interconnected gears. This rotation powers cams and dowels, which connect the motion to the ripple rings above, creating a gentle, cyclical movement. Each turn of the motor flows through this kinetic structure, symbolizing how a cherished object, like a raindrop in an ocean of memories, evokes waves of recollection. This mesmerizing ripple invites the user to share the story behind their item, fostering a meaningful connection with our robot.
<img src="https://github.com/user-attachments/assets/b8a0f5cc-cae8-4d3d-8a13-7e0fb8767a0e" width="299" height="744">
# Motor and Gear Structure
The main mechanical design is concentrated within the central podium, where a motor replaces the original servos of the robot. Using a mechanism of gears and cams for connection and support, this setup creates a completely new cyclical kinetic movement, distinct from the previous robot’s linear extension motion.

---
<img src="https://github.com/user-attachments/assets/fa3d22df-a998-4ad2-928d-d2c69f741e51" width="400" height="518">

### Motor
To achieve the ripple movement effect when users place their items on the podium, we replaced the original servo with a more powerful rolling motor to provide the necessary kinetic energy, simplifying the original four servos into a single motor to control the entire dynamic interaction.

### Gears
The gear mechanism functions as the core driver, transmitting power from a single motor to other components while effectively modulating force and speed. The main gear is fitted with a 608 bearing, which plays a crucial role in reducing friction and enhancing the stability of the gear’s rotation. This bearing allows for smoother, more controlled movement by supporting the gear’s axis and minimizing wear over time. The gears are arranged to amplify or reduce torque as needed, ensuring consistent, smooth motion. As the gears rotate, they transfer motor-driven motion to connected cams, which drive the ripple effect in the rings above by creating a steady up-and-down motion. This combination of gears, cams, and the 608 bearing optimizes both the fluidity and durability of the kinetic movement.

---
![mec4](https://github.com/user-attachments/assets/84d28d28-95f3-4f2e-bd55-fd537ac74066)
### Cams
The cams serve as mechanical converters, transforming the motor's continuous rotational motion into a reciprocating, vertical movement. The cam profile is strategically designed so that, as the cam rotates, it exerts variable force on a follower connected to the rings above. This follower translates the cam's rotational changes into up-and-down motion, creating a controlled ripple effect. To ensure stability in the cams' movement, a shaft has been incorporated, along with two 6002-RS bearings. The 6002-RS bearings provide additional support by reducing friction and absorbing radial and axial loads, which stabilizes the cam’s operation and minimizes wear. Together, the shaft and 6002-RS bearing maintain smooth, reliable motion, enhancing the durability and precision of the ripple effect.

The shaft that holds the Cams is hexagonal so that the cams can each be offset by 60° with respect to their neighbors. This provides the rippling effect.
![image](https://github.com/user-attachments/assets/4c11f527-d72c-4802-ae21-c6592afb1fda)


# Material Choice
We chose to use transparent acrylic for laser-cutting the cams, ripple rings, and dowels to evoke the effect of water droplets. The transparency also enhances the refractive quality of the LED lights soldered onto the interior walls, allowing the light to shine through more vividly. We painted the laser-cut exterior walls white to further reflect and amplify the LED lighting effect. Most parts, including the motor bracket and gears, are 3D-printed with PLA, a material stiff enough to ensure proper connection and smooth gear rotation. For the cam shaft, we opted for metal to provide added stability to the entire mechanical structure.

---
### Manufacturing Process
![manuf01](https://github.com/user-attachments/assets/1726dc3e-2a26-4de7-b8cb-baf85a47d5ae)
In implementing the physical robot, we carefully selected different materials. Initially, we experimented with laser-cut ripple rings using birch wood, but due to the opaque nature of wood, we decided to switch to transparent acrylic. This change, along with painting the exterior walls white, allows the LED light to shine through more effectively, enhancing the visual experience for participants and highlighting the interaction with the robot.
![manu02](https://github.com/user-attachments/assets/2f94e261-d9cc-4ae0-ad36-1b43967a15d4)
During the production process, we encountered some design errors, so ultimately, to improve precision and save time and materials, we chose to use 3D printing instead of wood. We also continually tested the LED effects and refined the material design to enhance overall stability and light transmission, ensuring that our final design concept was effectively realized.

---
#### LED Testing Process
https://github.com/user-attachments/assets/97cc142e-ad6d-4269-a75b-38898aa3d520


