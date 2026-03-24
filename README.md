# TLA+ Visualisation

## Installation

### Step 1. Clone this repository
~~~
git clone https://github.com/hd-chuong/winter-tla.git
~~~
### Step 2. Install Python
Ensure you have Python 3 installed in your computer. Python is needed to host a minimal REST Server. The demo needs a server because otherwise, the JSON loading component does not work.

### Step 3. Start up the Python simple Server

From your Terminal / PowerShell
~~~
python -m http.server 7999
~~~

### Step 4. Access the vis demo

From your browser

Viewing the graph-view
~~~
http://localhost:7999/graphview.html
~~~


Viewing the matrix-view
~~~
http://localhost:7999/matrixview.html
~~~

## Usage

There is an option to upload datasets into either graph view or matrix view. The datasets are stored in `datasets` folder

**Note**: All sample datasets can be loaded into both the `graphview` and `matrixview`.