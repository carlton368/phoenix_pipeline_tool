# Phoenix Pipeline Tool

![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.5.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

# Phoenix Pipeline Tool

A comprehensive pipeline tool designed for VFX artists, featuring three main components: **Loader**, **Publisher**, and **Saver**. This tool maximizes workflow efficiency and facilitates collaboration by minimizing technical overhead, allowing artists to focus on creative work.

---

## Table of Contents
1. [Key Features](#key-features)
2. [Technology Stack](#technology-stack)
3. [Installation Requirements](#installation-requirements)
4. [Project Structure](#project-structure)
5. [Future Improvements](#future-improvements)
6. [Development Team](#development-team)
7. [Project Duration](#project-duration)
8. [Key Benefits](#key-benefits)
9. [License](#license)

---

## Key Features

### 🔐 Login
- Login System using **ShotGrid authentication**
- **User Email–based Account** Identification
- Real-time User Information Retrieval via the ShotGrid API

### 🔄 Loader
- Personalized experience tailored to user roles and project requirements  
- **Unified version control** for assets and shots  
- **Seamless integration** with VFX software including Maya and Nuke  
- **User-friendly thumbnail-based** browsing interface  

### 💾 Saver
- Save work files to custom paths and **automatically upload** versions to ShotGrid  
- **Automated file naming** and path generation  
- Maintain work consistency and **save time** with automated file management  
- **Real-time intuitive UI** for monitoring work paths and file save status  

### 📤 Publisher

#### Maya Publisher
- **Reference file auto-updates**  
- **Automated slate generation** with project information using captured image sequences via Playblast  
- Automated workflows in 3D environment, including **turntable animation**  

#### Nuke Publisher
- **Node-based rendering** with automated slate generation  
- **Write and Write Geo node management** through tree widget interface  
- **Automated MOV and EXR rendering**  

---

## Installation Requirements
- **Python 3.9**
- **Required Libraries**:
  - PySide6 (6.5.1)
  - certifi (2023.7.22)
  - charset-normalizer (3.3.0)
  - idna (3.4)
  - requests (2.31.0)
  - shiboken6 (6.5.1)
  - shotgun-api3 (3.3.1)
  - urllib3 (2.0.4)

## Getting Started

### Prerequisites
```bash
Python 3.9
Maya 2023+
Nuke 13.0+
```

### Installation
1. Clone the repository
```bash
git clone https://github.com/carlton368/phoenix_pipeline_tool.git
```

2. Install required packages
```bash
pip install -r requirements.txt
```

### HOW TO START
1. Open your terminal and navigate to the directory:
```bash
cd phoenix_pipeline_tool
```

3. Run the following command:
```bash
python main.py 
```

## Project Structure
```
phoenix/
├── core/               # Core functionality
├── phoenix_main/       # Main application logic
├── ui/                 # UI components
├── Saver/             # Save management
├── Publisher/         # Publishing tools
├── Launcher/          # Application entry points
├── env/              # Environment configurations
└── lib/              # External libraries
```

## Future Development
- [ ] Extended software compatibility
- [ ] Enhanced logging system
- [ ] Expanded test coverage
- [ ] Performance optimization

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Development Team

| Name   | Profile        | GitHub Profile                                
|--------|-------------|---------------------------------------------
| Seyoung Kang   | Team Leader      | [@kangseyoung](https://github.com/kangseyoung)
| Yumi Kang   | Film Major (VP Operator)      | [@yumai054](https://github.com/yumai054)
| Gyeoul Kim   | Digital Media Major (3D Rigger)      | 
| Sunjin Yun   | Industrial Design Major      | 
| Wonjin Lee   | Film Major      | [@carlton368](https://github.com/carlton368)


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Made with ❤️ by Team Phoenix
