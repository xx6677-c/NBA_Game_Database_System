import os

def merge_sql_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(base_dir, 'backend', 'database')
    
    output_file = os.path.join(database_dir, 'all_procedures.sql')
    
    # List of files to merge in order
    files_to_merge = [
        'all_procedures.sql', # The base file (assuming it has the initial set)
        'add_delete_post_procedure.sql',
        'add_player_rankings_procedure.sql',
        'add_player_procedures.sql',
        'add_team_procedures.sql',
        'add_image_procedures.sql',
        'add_user_avatar_procedure.sql',
        'add_get_image_procedure.sql',
        'add_shop_procedures.sql'
    ]
    
    # Read the base file first
    base_content = ""
    base_file_path = os.path.join(database_dir, 'all_procedures.sql')
    if os.path.exists(base_file_path):
        with open(base_file_path, 'r', encoding='utf-8') as f:
            base_content = f.read()
    
    final_content = base_content
    
    # Append other files
    for filename in files_to_merge:
        if filename == 'all_procedures.sql':
            continue
            
        file_path = os.path.join(database_dir, filename)
        if os.path.exists(file_path):
            print(f"Merging {filename}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                final_content += "\n\n" + f"-- Merged from {filename}\n" + content
        else:
            print(f"Warning: {filename} not found.")
            
    # Write back to all_procedures.sql
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"Successfully merged all procedures into {output_file}")

if __name__ == '__main__':
    merge_sql_files()
