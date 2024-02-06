# PyCA: Cellular automaton in Python

The goal was to develope an open source software to recreate cellular automaton on different meshes (square, hex, voronoi). We wanted to simulate widely studied models, such as [Game of Life](https://web.stanford.edu/class/sts145/Library/life.pdf). For this purpose, we have decided to choose the Python programming language, because of its numerous libraries.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/) (version >= 3.6 recommended) <!-- F-strings https://peps.python.org/pep-0498/ -->
- [Pygame](https://www.pygame.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Imageio](https://imageio.readthedocs.io/en/stable/user_guide/installation.html)

### Installing

Clone the repository:

```
git clone https://github.com/kennyfh/PyCA.git
```

Setup the required dependencies:

```
pip install -e.
``` 


## Usage

Run the command `python scripts/main.py` to start our software tool.

## Contributing

We welcome contributions to this project! If you have an idea for a new feature or a bug fix, please open an issue in the [issue tracker](https://github.com/kennyfh/PyCA/issues).

Before submitting a pull request, please make sure that your code passes the linter and conforms to the project's coding standards.

## License

This project is licensed under the GNU General Public License version 3.0 (GPL-3.0). See the [LICENSE](LICENSE) file for details.

## Wiki

The project's GitHub wiki contains additional documentation and resources. You can access it [here](https://github.com/kennyfh/PyCA/wiki).

## Team
* Kenny Jesús Flores Huamán (kflores1 AT us.es)
* Teodoro Jiménez Lepe (teojimenezlepe AT hotmail.com)

## Project structure

```
├── .gitignore              # File to ignore files and directories in git
│ 
├── CITATION.cff            # Citation file for references
│ 
├── LICENSE                 # Project license file
│ 
├── pyproject.toml          # Python project configuration file
│ 
├── README.md               # README file with information about the project
│ 
├── requirements.txt        # File with project dependencies
│
├── docs                    # Directory for project documents
│
├── examples                # Directory for examples or sample files
│
└── scripts                 # Directory for scripts and source code
    ├── main.py             # Main project file
    │
    └── stages           
        ├── hexagon.py      
        ├── pixel_perfect_polygon_hitbox.py
        ├── square.py      
        └── stage.py   

```

## Acknowledgements

- This project would not have been possible without the amazing [Python](https://www.python.org/) programming language.
- We used [Pygame](https://www.pygame.org/) to build the graphics.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) was used for the user interface.
- Special thanks to the developers and maintainers of these open source libraries.
