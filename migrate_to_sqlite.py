import sqlite3                                                                                        
import json                                                                                           
import os                                                                                             
from datetime import datetime                                                                         
                                                                                                    
DB_NAME = "nomi_memory.db"                                                                            
CHATS_DIR = "chats"                                                                                   
                                                                                                    
def create_tables(cursor):                                                                            
    """Creates the database schema."""                                                                
    # Create chats table                                                                              
    cursor.execute("""                                                                                
    CREATE TABLE IF NOT EXISTS chats (                                                                
        id INTEGER PRIMARY KEY AUTOINCREMENT,                                                         
        name TEXT UNIQUE NOT NULL,                                                                    
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP                                                
    )                                                                                                 
    """)                                                                                              
    # Create messages table                                                                           
    cursor.execute("""                                                                                
    CREATE TABLE IF NOT EXISTS messages (                                                             
        id INTEGER PRIMARY KEY AUTOINCREMENT,                                                         
        chat_id INTEGER NOT NULL,                                                                     
        role TEXT NOT NULL,                                                                           
        content TEXT NOT NULL,                                                                        
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                                                
        FOREIGN KEY (chat_id) REFERENCES chats (id)                                                   
    )                                                                                                 
    """)                                                                                              
    print("Tables 'chats' and 'messages' created or already exist.")                                  
                                                                                                    
def migrate_chats():                                                                                  
    """Migrates all .json files from the chats directory to the SQLite DB."""                         
    conn = sqlite3.connect(DB_NAME)                                                                   
    cursor = conn.cursor()                                                                            
    create_tables(cursor)                                                                             
                                                                                                    
    json_files = [f for f in os.listdir(CHATS_DIR) if f.endswith(".json")]                            
                                                                                                    
    for file_name in json_files:                                                                      
        chat_name = os.path.splitext(file_name)[0]                                                    
        file_path = os.path.join(CHATS_DIR, file_name)                                                
                                                                                                    
        print(f"Migrating chat: {chat_name}...")                                                      
                                                                                                    
        # 1. Insert the chat into the 'chats' table                                                   
        try:                                                                                          
            cursor.execute("INSERT INTO chats (name) VALUES (?)", (chat_name,))                       
            chat_id = cursor.lastrowid                                                                
            print(f"  -> Created new chat entry with ID: {chat_id}")                                  
        except sqlite3.IntegrityError:                                                                
            # Chat already exists, let's find its ID and skip message insertion                       
            # to avoid duplicates if the script is run multiple times.                                
            print(f"  -> Chat '{chat_name}' already exists. Skipping migration.")                     
            continue # Move to the next file                                                          
                                                                                                    
        # 2. Load messages from JSON and insert them                                                  
        with open(file_path, "r", encoding="utf-8") as f:                                             
            history = json.load(f)                                                                    
                                                                                                    
        for message in history:                                                                       
            # Assuming the JSON format is a list of {'role': '...', 'parts': ['...']}                 
            role = message.get('role')                                                                
            content = message.get('parts', [''])[0] # Handle Gemini's 'parts' structure               
                                                                                                    
            if role and content:                                                                      
                cursor.execute(                                                                       
                    "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",                 
                    (chat_id, role, content)                                                          
                )                                                                                     
                                                                                                    
    conn.commit()                                                                                     
    conn.close()                                                                                      
    print("\nMigration complete! All chats are now in the SQLite database.")                          
                                                                                                    
if __name__ == "__main__":                                                                            
    if not os.path.exists(CHATS_DIR):                                                                 
        print(f"Error: Directory '{CHATS_DIR}' not found.")                                           
    else:                                                                                             
        migrate_chats()