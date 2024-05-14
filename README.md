### Set up project  
  
1. Clone the repository or download as zip and extract it.  
  
```  
git clone https://github.com/omkar-334/internal.git  
```  
  
2. Create a virtual environment  
  
```  
python -m venv .venv  
```  
  
3. Activate .venv   
  IMPORTANT - remember to activate it each time you open terminal.  
```  
.venv\Scripts\activate  
```  
  
4. Install required libraries.  
  
```python  
pip install -r requirements.txt
```

5. Add LAB name and TOPICS to `.env`.  
   This will give the LLM more context. This is optional.  
   KEEP EMPTY IF you don't want. IT WILL INFLUENCE RESPONSES.
   Do NOT add any quotation marks.  
   example -  
   ```
   LAB=Internet Technologies Lab
   TOPICS=React, React table, React form, React props, functions, ES5 vs ES6
   ```

7. Run Script 
  
```python  
python main.py
``` 
