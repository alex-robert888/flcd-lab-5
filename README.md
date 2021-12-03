# Parsing 

## Goals

1. Process any kind of formal grammar, with some basic functionalities.
2. Given any context-free grammar (eg. a basic grammar or the grammar of a programming language), parse any sequence / a source code and generate the parse tree.

## General Approach & Parsing Method

We designed two primary models:

1. **Grammar** - a class for loading and processing any kind of formal grammar from an input file (see the input file format below).
2. **Parser** - a class representing the parse and holding all the correponding data strucures.

The parser receives a reference to the grammar as well as to the Program Internal Form of the input sample and builds an according parsing tree

## Parsing Tree Representation

The parsing tree is implemented using a **table based on the parent-sibling relationships** for each of the nodes.

Each node describes a symbol in the context of the sample program and the formal grammar.

![image](https://user-images.githubusercontent.com/52594991/144616103-4978a3a5-f526-4b7a-b6d5-f4e57a833499.png)

## Parser Data Structures

* Parsing Tree (build after parsing)
* Grammar (formal grammar)
* Program Internal Form (PIF of the input program written in the minilanguage depicted by the grammar)
* Input Stack (holds the currently processed part of the tree)
* Working Stack (stores the parsed symbols)
* Current State (parser can be in any of the following 4 states: NORMAL, BACK, ERROR, FINAL)
* Position of the Current Symbol

## Parser Operations

### 1. Expand

When in normal state and a non-terminal is currenty processed (is on the top of the input stack):
   1. push the first production of the symbol into the working stack
   2. push the symbols corresponding to the firt production into the input stack

![image](https://user-images.githubusercontent.com/52594991/144620319-862ff1a3-9b99-4a39-bf1d-e3c5adfe6a1f.png)

### 2. Advance

When in normal state and a terminal is currently processed (is on the top of the input stack):
   1. increment the position of the current symbol
   2. push the current terminal into the working stack

![image](https://user-images.githubusercontent.com/52594991/144620381-16193216-1fc5-4fd6-a49c-55bc0ab1bcd6.png)

### 3. Momentary Insuccess

When in normal state, head of the input stack is a terminal, which is different from the current symbol from the PIF:
  1. set the current state to back


![image](https://user-images.githubusercontent.com/52594991/144620467-777b5dc7-4d23-495a-8c42-029f33b10636.png)

### 4. Back

When in back state and the head of the input stack is a termnal;
  1. decrement the position of the currently processed symbol
  2. pop the the top of the working stack and push it to the input stack

![image](https://user-images.githubusercontent.com/52594991/144620535-86e39d68-34b1-42d1-95a4-813bbe42febc.png)

### 5. Another Try

When in back state, head of the input stack is a terminal, which is different from the current symbol from the PIF:
  1. try with the next symbol from the currently processed production if there is any next
  2. if there is no other symbol in the currently processsed production, set the current state to back and go to the next production if possible
  3. set current state to error recursivity back-tracked to the starting position of the tree.

![image](https://user-images.githubusercontent.com/52594991/144620605-64f6c56f-3838-41cf-a532-b2c43094d613.png)

### 6. Success
![image](https://user-images.githubusercontent.com/52594991/144620670-cb8ced70-d1fe-4b0a-a7ed-f3464dc064e0.png)

When in normal state:
  1. set the current state to success

## Grammar Input File Format

The format of the input file is the following:
* the set of non-terminal symbols will be listed on the first line (separated by spaces)
* the set of terminal symbols will be listed on the second line (separated by spaces)
* the starting symbol will be placed on the third line
* and all the remaining lines will describe the production, in the following fashion: `<list_of_left_side_symbols> - <list_right_side_symbols>`

## Input Files Examples
### g1.txt - a simple grammar
![image](https://user-images.githubusercontent.com/52594991/142611694-8f579db8-0884-4504-80ca-78418d2ed7df.png)

### g2.txt - grammar of the mini-language
![image](https://user-images.githubusercontent.com/52594991/144614412-3101203e-18a7-4a0d-b163-c51ae109e404.png)

## Documented Tests

https://docs.google.com/document/d/1oU9ng29mMsg5npG1JqTqawmowtTcaUoNPld3HyvkwxE/edit?usp=sharing

## Class Diagram

![ClassDiagram](https://user-images.githubusercontent.com/52594991/144623950-114dc68d-37cd-40b7-8c87-179daf652bb5.jpeg)

