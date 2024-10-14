**Lecture 4: Functions and Scope**
=====================================

**Introduction**
---------------

In this lecture, we will continue to explore the concept of functions in Python. We will discuss the difference between `print` and `return`, and how to nest functions within each other. We will also review the concept of scope and how it relates to functions.

**Quick Recap of Previous Lecture**
-----------------------------------

In the previous lecture, we covered more string manipulations and introduced the concept of functions. We discussed how to define and call functions, and how to use the `Python Tutor` tool to visualize the execution of code.

**Example: Print vs Return and Nested Functions**
-----------------------------------------------

Let's consider an example that demonstrates the difference between `print` and `return`, as well as nested functions.
```python
def g(x):
    def h():
        x = 'abc'
    x = x + 1
    print('Inside g')
    h()
    return x

x = 3
z = g(x)
```
**Step-by-Step Execution**
---------------------------

Let's go through the execution of this code step by step:

1. We define a function `g` that takes an argument `x`.
2. Inside `g`, we define another function `h`.
3. We assign `x` to be `3` in the global scope.
4. We call `g` with `x` as an argument, and assign the result to `z`.
5. Inside `g`, we increment `x` to be â€œ4â€.
6. We print out the message "Inside g".
7. We call `h()`, which defines a new scope.
8. Inside `h`, we assign `x` to be the string `'abc'`.
9. Since there is no `return` statement in `h`, it returns `None` by default.
10. We return to the scope of `g`, and replace the call to `h()` with `None`.
11. We return `x` from `g`, which is now â€œ4â€.
12. We assign the result of `g(x)` to `z` in the global scope.

**Key Takeaways**
----------------

* `print` and `return` are two different concepts in Python. `print` outputs a value to the console, while `return` returns a value from a function.
* Functions can be nested within each other, and each function has its own scope.
* When a function is called, a new scope is created, and variables are mapped to their corresponding values.

**Decomposition and Abstraction**
--------------------------------

Functions are a powerful tool for decomposition and abstraction in programming. By defining our own functions, we can write clean and simple code that is easy to debug and reuse.

**Conclusion**
----------

In this lecture, we covered the basics of functions in Python, including the difference between `print` and `return`, and how to nest functions within each other. We also discussed the concept of scope and how it relates to functions. With this knowledge, you should be able to write more efficient and effective code using functions.

**Points to Ponder**
-------------------

* What are the advantages of using functions in programming?
* How do functions help with decomposition and abstraction?
* What is the difference between `print` and `return` in Python?

**Key Concepts**
----------------

* Functions
* Scope
* Print vs Return
* Nested Functions
* Decomposition
* Abstraction

**References**
--------------

* Python Tutor: <https://pythontutor.com/>
* MIT OpenCourseWare: <https://ocw.mit.edu/>