# Scientific Calculator with Streamlit
# File: scientific_calculator.py

import streamlit as st
import math
import numpy as np
from decimal import Decimal, InvalidOperation

# Page configuration
st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        margin: 2px;
    }
    .number-btn button {
        background-color: #f0f2f6;
    }
    .operator-btn button {
        background-color: #ff6b6b;
        color: white;
    }
    .function-btn button {
        background-color: #4ecdc4;
        color: white;
    }
    .equals-btn button {
        background-color: #95e1d3;
        font-size: 24px;
    }
    .display {
        background-color: #2c3e50;
        color: #ecf0f1;
        padding: 20px;
        border-radius: 10px;
        font-size: 28px;
        text-align: right;
        margin-bottom: 20px;
        font-family: 'Courier New', monospace;
        min-height: 80px;
        word-wrap: break-word;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'memory' not in st.session_state:
    st.session_state.memory = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# Calculator functions
class ScientificCalculator:
    
    @staticmethod
    def evaluate(expression):
        """Safely evaluate mathematical expression"""
        try:
            # Replace common math functions
            expression = expression.replace('^', '**')
            expression = expression.replace('π', str(math.pi))
            expression = expression.replace('e', str(math.e))
            
            # Create safe namespace for eval
            safe_dict = {
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
                'log': math.log10, 'ln': math.log, 'log10': math.log10,
                'sqrt': math.sqrt, 'pow': math.pow,
                'exp': math.exp, 'factorial': math.factorial,
                'pi': math.pi, 'e': math.e,
                'abs': abs, 'round': round,
                'ceil': math.ceil, 'floor': math.floor,
                'degrees': math.degrees, 'radians': math.radians,
                '__builtins__': {}
            }
            
            result = eval(expression, safe_dict)
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def scientific_function(func_name, value):
        """Apply scientific function to value"""
        try:
            value = float(value)
            functions = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
                'log': math.log10,
                'ln': math.log,
                'sqrt': math.sqrt,
                'square': lambda x: x**2,
                'cube': lambda x: x**3,
                'reciprocal': lambda x: 1/x,
                'factorial': math.factorial,
                'abs': abs,
                'exp': math.exp,
                'deg': math.degrees,
                'rad': math.radians,
                'ceil': math.ceil,
                'floor': math.floor
            }
            
            if func_name in functions:
                result = functions[func_name](value)
                return str(result)
            return "Error"
        except Exception as e:
            return f"Error: {str(e)}"

calc = ScientificCalculator()

# Main title
st.title("🧮 Scientific Calculator")

# Display
st.markdown(f'<div class="display">{st.session_state.display}</div>', unsafe_allow_html=True)

# Calculator mode selection
mode = st.sidebar.selectbox("Mode", ["Standard", "Scientific", "Programmer"])

# Memory display
if st.session_state.memory != 0:
    st.sidebar.info(f"Memory: {st.session_state.memory}")

# History
if st.session_state.history:
    with st.sidebar.expander("📜 History"):
        for item in reversed(st.session_state.history[-10:]):
            st.text(item)
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

# Button click handler
def button_click(value):
    if st.session_state.display == '0' and value not in ['+', '-', '*', '/', '^']:
        st.session_state.display = str(value)
    else:
        st.session_state.display += str(value)

def clear():
    st.session_state.display = '0'

def clear_entry():
    st.session_state.display = st.session_state.display[:-1]
    if not st.session_state.display:
        st.session_state.display = '0'

def calculate():
    try:
        expression = st.session_state.display
        result = calc.evaluate(expression)
        
        if not isinstance(result, str) or not result.startswith("Error"):
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            # Add to history
            st.session_state.history.append(f"{expression} = {result}")
            st.session_state.display = str(result)
        else:
            st.session_state.display = result
    except Exception as e:
        st.session_state.display = f"Error: {str(e)}"

def apply_function(func):
    try:
        current_value = st.session_state.display
        result = calc.scientific_function(func, current_value)
        st.session_state.display = result
    except Exception as e:
        st.session_state.display = f"Error: {str(e)}"

def memory_add():
    try:
        st.session_state.memory += float(st.session_state.display)
    except:
        pass

def memory_subtract():
    try:
        st.session_state.memory -= float(st.session_state.display)
    except:
        pass

def memory_recall():
    st.session_state.display = str(st.session_state.memory)

def memory_clear():
    st.session_state.memory = 0

# Standard Calculator Layout
if mode == "Standard":
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("C", key="clear", help="Clear"):
            clear()
        if st.button("7", key="7"):
            button_click(7)
        if st.button("4", key="4"):
            button_click(4)
        if st.button("1", key="1"):
            button_click(1)
        if st.button("0", key="0"):
            button_click(0)
    
    with col2:
        if st.button("CE", key="ce", help="Clear Entry"):
            clear_entry()
        if st.button("8", key="8"):
            button_click(8)
        if st.button("5", key="5"):
            button_click(5)
        if st.button("2", key="2"):
            button_click(2)
        if st.button(".", key="dot"):
            button_click('.')
    
    with col3:
        if st.button("÷", key="div"):
            button_click('/')
        if st.button("9", key="9"):
            button_click(9)
        if st.button("6", key="6"):
            button_click(6)
        if st.button("3", key="3"):
            button_click(3)
        if st.button("=", key="equals"):
            calculate()
    
    with col4:
        if st.button("×", key="mult"):
            button_click('*')
        if st.button("−", key="minus"):
            button_click('-')
        if st.button("+", key="plus"):
            button_click('+')
        if st.button("√", key="sqrt"):
            apply_function('sqrt')
        if st.button("x²", key="square"):
            apply_function('square')

# Scientific Calculator Layout
elif mode == "Scientific":
    
    # Row 1: Memory and Clear
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("MC", key="mc"):
            memory_clear()
    with col2:
        if st.button("MR", key="mr"):
            memory_recall()
    with col3:
        if st.button("M+", key="m_add"):
            memory_add()
    with col4:
        if st.button("M−", key="m_sub"):
            memory_subtract()
    with col5:
        if st.button("C", key="clear_sci"):
            clear()
    
    # Row 2: Trigonometric functions
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("sin", key="sin"):
            apply_function('sin')
    with col2:
        if st.button("cos", key="cos"):
            apply_function('cos')
    with col3:
        if st.button("tan", key="tan"):
            apply_function('tan')
    with col4:
        if st.button("π", key="pi"):
            button_click('π')
    with col5:
        if st.button("e", key="e"):
            button_click('e')
    
    # Row 3: Inverse trig and log
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("asin", key="asin"):
            apply_function('asin')
    with col2:
        if st.button("acos", key="acos"):
            apply_function('acos')
    with col3:
        if st.button("atan", key="atan"):
            apply_function('atan')
    with col4:
        if st.button("log", key="log"):
            apply_function('log')
    with col5:
        if st.button("ln", key="ln"):
            apply_function('ln')
    
    # Row 4: Powers and roots
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("x²", key="square_sci"):
            apply_function('square')
    with col2:
        if st.button("x³", key="cube"):
            apply_function('cube')
    with col3:
        if st.button("xʸ", key="power"):
            button_click('^')
    with col4:
        if st.button("√", key="sqrt_sci"):
            apply_function('sqrt')
    with col5:
        if st.button("1/x", key="reciprocal"):
            apply_function('reciprocal')
    
    # Row 5: Numbers and operators
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("7", key="7_sci"):
            button_click(7)
    with col2:
        if st.button("8", key="8_sci"):
            button_click(8)
    with col3:
        if st.button("9", key="9_sci"):
            button_click(9)
    with col4:
        if st.button("÷", key="div_sci"):
            button_click('/')
    with col5:
        if st.button("n!", key="factorial"):
            apply_function('factorial')
    
    # Row 6
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("4", key="4_sci"):
            button_click(4)
    with col2:
        if st.button("5", key="5_sci"):
            button_click(5)
    with col3:
        if st.button("6", key="6_sci"):
            button_click(6)
    with col4:
        if st.button("×", key="mult_sci"):
            button_click('*')
    with col5:
        if st.button("(", key="open_paren"):
            button_click('(')
    
    # Row 7
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("1", key="1_sci"):
            button_click(1)
    with col2:
        if st.button("2", key="2_sci"):
            button_click(2)
    with col3:
        if st.button("3", key="3_sci"):
            button_click(3)
    with col4:
        if st.button("−", key="minus_sci"):
            button_click('-')
    with col5:
        if st.button(")", key="close_paren"):
            button_click(')')
    
    # Row 8
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("0", key="0_sci"):
            button_click(0)
    with col2:
        if st.button(".", key="dot_sci"):
            button_click('.')
    with col3:
        if st.button("±", key="sign"):
            try:
                val = float(st.session_state.display)
                st.session_state.display = str(-val)
            except:
                pass
    with col4:
        if st.button("+", key="plus_sci"):
            button_click('+')
    with col5:
        if st.button("=", key="equals_sci"):
            calculate()

# Programmer Mode
elif mode == "Programmer":
    st.info("🔧 Programmer mode - Binary, Octal, Hex conversions")
    
    # Number system converter
    col1, col2 = st.columns(2)
    
    with col1:
        input_base = st.selectbox("Input Base", ["Decimal", "Binary", "Octal", "Hexadecimal"])
        input_value = st.text_input("Enter value", value="0")
    
    with col2:
        output_base = st.selectbox("Output Base", ["Binary", "Octal", "Decimal", "Hexadecimal"])
    
    if st.button("Convert"):
        try:
            # Convert input to decimal
            base_map = {"Decimal": 10, "Binary": 2, "Octal": 8, "Hexadecimal": 16}
            decimal_value = int(input_value, base_map[input_base])
            
            # Convert decimal to output base
            if output_base == "Binary":
                result = bin(decimal_value)
            elif output_base == "Octal":
                result = oct(decimal_value)
            elif output_base == "Hexadecimal":
                result = hex(decimal_value)
            else:
                result = str(decimal_value)
            
            st.success(f"Result: {result}")
        except ValueError:
            st.error("Invalid input for selected base")
    
    # Bitwise operations
    st.markdown("---")
    st.subheader("Bitwise Operations")
    
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("Number 1", value=0, step=1)
    with col2:
        num2 = st.number_input("Number 2", value=0, step=1)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("AND"):
            st.session_state.display = str(int(num1) & int(num2))
    with col2:
        if st.button("OR"):
            st.session_state.display = str(int(num1) | int(num2))
    with col3:
        if st.button("XOR"):
            st.session_state.display = str(int(num1) ^ int(num2))
    with col4:
        if st.button("NOT"):
            st.session_state.display = str(~int(num1))

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | Scientific Calculator v1.0")
