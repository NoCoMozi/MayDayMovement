import os
import json
from datetime import datetime
import re
from bs4 import BeautifulSoup

def create_update_card(content, date):
    return f'''
    <div class="col-md-12 mb-4">
        <div class="card">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h5 class="card-title">Update</h5>
                    <small class="text-muted">{date}</small>
                </div>
                <p class="card-text">{content}</p>
            </div>
        </div>
    </div>
    '''

def main():
    # Get update content from environment variables
    content = os.environ.get('UPDATE_CONTENT')
    date = os.environ.get('UPDATE_DATE', datetime.now().strftime('%Y-%m-%d %H:%M'))

    if not content:
        print("No content provided")
        return

    # Read the current index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the updates container
    updates_container = soup.find(id='updates-container')
    
    # Create new update card
    new_card = BeautifulSoup(create_update_card(content, date), 'html.parser')
    
    # Insert the new card at the beginning
    first_card = updates_container.find('div', class_='col-md-12')
    if first_card:
        first_card.insert_before(new_card)
    else:
        updates_container.append(new_card)

    # Save the updated HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

    # Also save update to a JSON file
    update_data = {
        'content': content,
        'date': date
    }
    
    # Create unique filename based on timestamp
    filename = f"updates/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(update_data, f, indent=2)

if __name__ == "__main__":
    main()
