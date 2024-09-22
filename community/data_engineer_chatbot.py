import json
import requests

stream = False
url = "https://proxy.tune.app/chat/completions"
headers = {
    "Authorization": "sk-tune-a56yPBs8RNJSQYgaOU9F9wPMExWu02zZq6w",
    "Content-Type": "application/json",
}
data = {
  "temperature": 0.8,
    "messages":  [
  {
    "role": "system",
    "content": "Give me set of rules step by step that i need to take care of while doing data engineering project"
  },
  {
    "role": "user",
    "content": "1. understand the data first\n2. know the bussiness goal\n3. understand the bussiness goal \n4. understand technical analysis and feasilblity \n5. plan the architect\n6. create a poc\n7. develop phase 1\n8. do data auditing\n9. work on phase 2 and improvements\n10. do data auditing\n11. implement data QA \n12.  test the pipeline for all environments\n13. release the pipeline.\n"
  },
  {
    "role": "user",
    "content": "help me to understand data "
  },
  {
    "role": "assistant",
    "content": "Understanding data is a crucial step in any data-driven project. Here are some steps and tips to help you understand data better:\n\n### 1. **Define Objectives**\n   - **Identify Goals:** Understand the business goals and how the data will help in achieving those goals.\n   - **Key Questions:** Determine the key questions that need to be addressed with the data.\n\n### 2. **Collect Data**\n   - **Data Sources:** Identify all potential data sources (e.g., databases, APIs, files).\n   - **Data Collection Methods:** Understand how the data is collected and ensure it’s reliable.\n\n### 3. **Data Types and Formats**\n   - **Data Types:** Identify the types of data you have (e.g., numerical, categorical, text).\n   - **Data Formats:** Check the formats of your data (e.g., CSV, JSON, SQL databases).\n\n### 4. **Data Exploration**\n   - **Initial Analysis:** Perform an initial analysis to get a basic understanding (mean, median, mode, standard deviation).\n   - **Data Visualization:** Use visualization tools to see patterns (e.g., histograms, scatter plots, box plots).\n\n### 5. **Data Quality Assessment**\n   - **Missing Data:** Identify and handle missing data appropriately (e.g., imputation, deletion).\n   - **Outliers:** Detect outliers and understand their impact.\n   - **Consistency:** Check for consistency in data entries.\n\n### 6. **Data Cleaning**\n   - **Remove Duplicates:** Ensure there are no duplicate entries.\n   - **Correct Errors:** Fix any errors or inconsistencies in the data.\n   - **Standardize:** Standardize data formats for uniformity.\n\n### 7. **Data Transformation**\n   - **Normalization/Standardization:** Transform data to a consistent scale, if necessary.\n   - **Feature Engineering:** Create new features that may provide better insights.\n\n### 8. **Documentation**\n   - **Data Dictionary:** Create a data dictionary describing each feature, including its meaning, type, and any data transformations applied.\n   - **Metadata:** Document any metadata, such as data source, collection date, and any preprocessing steps.\n\n### 9. **Tools & Techniques**\n   - **Tools:** Use tools like Python (Pandas, NumPy), R, SQL, Excel for data analysis and cleaning.\n   - **Visualization:** Use visualization libraries like Matplotlib, Seaborn, and tools like Tableau for visual insights.\n\n### Examples of Tools and Techniques:\n- **Python Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn\n- **Database Queries:** SQL for querying and manipulating data\n- **Visualization Tools:** Tableau, Power BI\n\n### Example Python Code for Data Exploration:\n```python\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n# Load the dataset\ndata = pd.read_csv('your_data.csv')\n\n# Display basic information\nprint(data.info())\n\n# Summary statistics\nprint(data.describe())\n\n# Check for missing values\nprint(data.isnull().sum())\n\n# Data visualization\nplt.figure(figsize=(10, 6))\nsns.histplot(data['some_feature'], kde=True)\nplt.show()\n```\n\nWould you like a more detailed explanation on any of these steps or specific help with your dataset?"
  },
  {
    "role": "user",
    "content": "help me understand data auditing"
  },
  {
    "role": "assistant",
    "content": "Data auditing is a critical process to ensure the integrity, quality, and compliance of data. It involves reviewing and validating the data to identify any issues or anomalies. Here are the steps and tips to help you perform data auditing effectively:\n\n### Steps for Data Auditing\n\n#### 1. **Define Objectives and Scope**\n   - **Objectives:** Clearly define what you aim to achieve with data auditing (e.g., data accuracy, completeness, compliance).\n   - **Scope:** Determine the scope of the audit, including which datasets and specific fields will be audited.\n\n#### 2. **Data Collection and Sampling**\n   - **Collect Data:** Gather the data you need to audit from various sources.\n   - **Sampling:** If dealing with large datasets, consider using sampling techniques to audit a representative subset of the data.\n\n#### 3. **Data Validation**\n   - **Accuracy:** Check if the data values are correct and reflect the real-world entities or events they are supposed to represent.\n   - **Completeness:** Ensure that no required data is missing and that all expected records are present.\n   - **Consistency:** Verify that the data is consistent across different datasets and systems.\n   - **Uniqueness:** Ensure that there are no duplicate records in the dataset.\n\n#### 4. **Data Quality Checks**\n   - **Range Checks:** Verify that numerical values fall within expected ranges.\n   - **Format Checks:** Ensure that the data follows the correct format (e.g., date formats, email formats).\n   - **Referential Integrity:** Ensure that all references between datasets are valid (e.g., foreign keys in databases).\n\n#### 5. **Data Anomaly Detection**\n   - **Outliers:** Identify and investigate any outliers or unusual data points.\n   - **Patterns:** Look for unexpected patterns that might indicate data issues or fraud.\n\n#### 6. **Documentation and Reporting**\n   - **Record Findings:** Document any issues or anomalies found during the audit.\n   - **Reporting:** Create a detailed report outlining the findings, including the nature of the issues, their possible causes, and recommended actions.\n\n#### 7. **Action and Follow-Up**\n   - **Corrective Actions:** Implement corrective actions to address any identified issues.\n   - **Follow-Up:** Schedule follow-up audits to ensure that the corrective actions were effective and the data quality has improved.\n\n### Tools and Techniques for Data Auditing\n\n- **SQL and Databases:** Use SQL queries to validate data integrity and perform quality checks.\n- **Python Libraries:** Utilize Python libraries like Pandas, NumPy, and Scipy for data analysis and anomaly detection.\n- **Data Visualization:** Tools like Tableau, Power BI, or Python libraries (Matplotlib, Seaborn) can help visualize data issues.\n- **Automated Tools:** Consider using data quality and auditing tools like Talend, Informatica, or Apache Griffin.\n\n### Example Python Code for Data Auditing\nHere’s a simple example using Python to perform basic data auditing tasks:\n\n```python\nimport pandas as pd\nimport numpy as np\n\n# Load the dataset\ndata = pd.read_csv('your_data.csv')\n\n# Check for missing values\nmissing_values = data.isnull().sum()\nprint(\"Missing Values:\\n\", missing_values)\n\n# Check for duplicates\nduplicates = data.duplicated().sum()\nprint(\"Duplicate Records:\", duplicates)\n\n# Range checks (example for a column 'age')\nage_out_of_range = data[(data['age'] < 0) | (data['age'] > 120)]\nprint(\"Age Out of Range:\\n\", age_out_of_range)\n\n# Format checks (example for an 'email' column)\nimport re\ndef check_email_format(email):\n    regex = r'^\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'\n    return re.match(regex, email)\n\ninvalid_emails = data[~data['email'].apply(lambda x: bool(check_email_format(x)))]\nprint(\"Invalid Email Formats:\\n\", invalid_emails)\n\n# Outlier detection (example for a numerical column 'salary')\nQ1 = data['salary'].quantile(0.25)\nQ3 = data['salary'].quantile(0.75)\nIQR = Q3 - Q1\noutliers = data[(data['salary'] < (Q1 - 1.5 * IQR)) | (data['salary'] > (Q3 + 1.5 * IQR))]\nprint(\"Outliers:\\n\", outliers)\n```\n\n### Key Considerations\n\n- **Regular Audits:** Schedule regular audits to maintain data quality.\n- **Stakeholder Involvement:** Involve relevant stakeholders to understand the context and impact of data issues.\n- **Automate Where Possible:** Use automated tools and scripts to streamline the auditing process.\n\nWould you like help with a specific part of data auditing or need more detailed examples?"
  }
],
    "model": "kaushikaakash04/tune-blob",
    "stream": stream,
    "frequency_penalty":  0,
    "max_tokens": 900
}
response = requests.post(url, headers=headers, json=data)
if stream:
    for line in response.iter_lines():
        if line:
            l = line[6:]
            if l != b'[DONE]':
              print(json.loads(l))
else:
  print(response.json())