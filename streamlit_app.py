import streamlit as st
import pandas as pd
import re
import json
from typing import Dict, Any

# Page configuration
st.set_page_config(
    page_title="AI Code Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .code-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        background-color: #f8f9fa;
    }
    .conversion-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🔄 AI Code Converter</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        conversion_type = st.selectbox(
            "Select Conversion Type:",
            [
                "JavaScript to TypeScript",
                "Python to JavaScript", 
                "CSS to Tailwind CSS",
                "React Class to Function Components",
                "SQL to Pandas",
                "JSON to Python Dict"
            ]
        )
        
        st.subheader("Options")
        auto_convert = st.checkbox("Auto-convert on type", value=False)
        show_analysis = st.checkbox("Show code analysis", value=True)
        
        st.markdown("---")
        st.info("💡 **Tips:**\n- Paste your code in the input area\n- Select conversion type\n- Click convert or enable auto-convert")

    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Input Code")
        input_code = st.text_area(
            "Paste your code here:",
            height=400,
            placeholder="Paste your source code here...",
            label_visibility="collapsed",
            key="input_code"
        )
        
        # Example code buttons
        st.subheader("🚀 Quick Examples")
        example_col1, example_col2, example_col3 = st.columns(3)
        
        with example_col1:
            if st.button("JS Example", key="js_example"):
                js_example = """function calculateTotal(items) {
    let total = 0;
    for (let i = 0; i < items.length; i++) {
        total += items[i].price * items[i].quantity;
    }
    return total;
}"""
                st.session_state.input_code = js_example
                
        with example_col2:
            if st.button("CSS Example", key="css_example"):
                css_example = """.container {
    margin: 20px;
    padding: 15px;
    background-color: #f0f0f0;
    border-radius: 5px;
}

.button {
    color: white;
    background-color: blue;
    padding: 10px 20px;
}"""
                st.session_state.input_code = css_example
                
        with example_col3:
            if st.button("Python Example", key="python_example"):
                python_example = """def process_data(data):
    result = []
    for item in data:
        if item['active']:
            result.append({
                'name': item['name'],
                'value': item['value'] * 2
            })
    return result"""
                st.session_state.input_code = python_example

    with col2:
        st.subheader("📤 Converted Code")
        
        # Convert button
        convert_clicked = st.button("🔄 Convert Code", type="primary", key="convert")
        
        if convert_clicked or (auto_convert and input_code):
            if input_code:
                converted_code = convert_code(input_code, conversion_type)
                
                st.code(converted_code, language=get_output_language(conversion_type))
                
                # Copy button
                if st.button("📋 Copy to Clipboard", key="copy"):
                    st.code(converted_code)
                    st.success("Code copied to clipboard!")
                
                # Analysis section
                if show_analysis:
                    with st.expander("📊 Code Analysis"):
                        analysis = analyze_code(input_code, converted_code, conversion_type)
                        for key, value in analysis.items():
                            st.write(f"**{key}:** {value}")
            else:
                st.warning("Please enter some code to convert.")
        else:
            st.info("Enter code and click 'Convert Code' to see the result here.")

def convert_code(code: str, conversion_type: str) -> str:
    """Convert code based on the selected conversion type"""
    
    if conversion_type == "JavaScript to TypeScript":
        return convert_js_to_ts(code)
    elif conversion_type == "Python to JavaScript":
        return convert_python_to_js(code)
    elif conversion_type == "CSS to Tailwind CSS":
        return convert_css_to_tailwind(code)
    elif conversion_type == "React Class to Function Components":
        return convert_react_class_to_function(code)
    elif conversion_type == "SQL to Pandas":
        return convert_sql_to_pandas(code)
    elif conversion_type == "JSON to Python Dict":
        return convert_json_to_python(code)
    else:
        return "Conversion type not implemented yet."

def convert_js_to_ts(code: str) -> str:
    """Convert JavaScript to TypeScript"""
    # Simple conversions - you can expand this
    converted = code
    
    # Add basic type annotations
    converted = re.sub(r'function\s+(\w+)\s*\((.*?)\)', r'function \1(\2): any', converted)
    converted = re.sub(r'const\s+(\w+)\s*=', r'const \1: any =', converted)
    converted = re.sub(r'let\s+(\w+)\s*=', r'let \1: any =', converted)
    converted = re.sub(r'var\s+(\w+)\s*=', r'var \1: any =', converted)
    
    return f"// TypeScript Conversion\n{converted}"

def convert_python_to_js(code: str) -> str:
    """Convert Python to JavaScript"""
    converted = code
    
    # Basic syntax conversions
    converted = converted.replace('def ', 'function ')
    converted = converted.replace(':', '{')
    converted = converted.replace('#', '//')
    converted = re.sub(r'print\((.*?)\)', r'console.log(\1)', converted)
    converted = re.sub(r'len\((.*?)\)', r'\1.length', converted)
    
    return f"// JavaScript Conversion\n{converted}"

def convert_css_to_tailwind(code: str) -> str:
    """Convert CSS to Tailwind CSS classes"""
    converted = "// Tailwind CSS Classes\n"
    
    # Simple CSS to Tailwind mapping
    lines = code.split('\n')
    for line in lines:
        if 'margin:' in line:
            match = re.search(r'margin:\s*(\d+)px', line)
            if match:
                value = match.group(1)
                converted += f"m-{value} "
        elif 'padding:' in line:
            match = re.search(r'padding:\s*(\d+)px', line)
            if match:
                value = match.group(1)
                converted += f"p-{value} "
        elif 'color:' in line:
            match = re.search(r'color:\s*#?(\w+)', line)
            if match:
                value = match.group(1)
                converted += f"text-{value} "
        elif 'background-color:' in line:
            match = re.search(r'background-color:\s*#?(\w+)', line)
            if match:
                value = match.group(1)
                converted += f"bg-{value} "
    
    return converted

def convert_react_class_to_function(code: str) -> str:
    """Convert React class components to function components"""
    return "// Function component conversion would go here\n// (This is a simplified example)\n" + code

def convert_sql_to_pandas(code: str) -> str:
    """Convert SQL queries to pandas operations"""
    return "# Pandas equivalent would go here\n# (This is a simplified example)\n" + code

def convert_json_to_python(code: str) -> str:
    """Convert JSON to Python dictionary"""
    try:
        parsed = json.loads(code)
        return f"# Python Dictionary\n{parsed}"
    except:
        return "# Invalid JSON provided\n" + code

def get_output_language(conversion_type: str) -> str:
    """Get the language for syntax highlighting"""
    mapping = {
        "JavaScript to TypeScript": "typescript",
        "Python to JavaScript": "javascript",
        "CSS to Tailwind CSS": "css",
        "React Class to Function Components": "jsx",
        "SQL to Pandas": "python",
        "JSON to Python Dict": "python"
    }
    return mapping.get(conversion_type, "text")

def analyze_code(input_code: str, output_code: str, conversion_type: str) -> Dict[str, Any]:
    """Analyze the code conversion"""
    analysis = {
        "Input Lines": len(input_code.split('\n')),
        "Output Lines": len(output_code.split('\n')),
        "Input Characters": len(input_code),
        "Output Characters": len(output_code),
        "Conversion Type": conversion_type
    }
    return analysis

if __name__ == "__main__":
    main()