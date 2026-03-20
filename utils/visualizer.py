# utils/visualizer.py
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

def create_pie_chart(data, title="Spam vs Ham Distribution"):
    """
    Create a pie chart from spam/ham data
    """
    if isinstance(data, str):
        # If data is a file path, load it
        df = pd.read_csv(data, encoding='latin-1')
        spam_count = (df['v1'] == 'spam').sum()
        ham_count = (df['v1'] == 'ham').sum()
    else:
        # If data is already counts
        spam_count, ham_count = data
    
    labels = ['Ham', 'Spam']
    sizes = [ham_count, spam_count]
    colors = ['#28a745', '#dc3545']
    explode = (0, 0.1)  # explode the spam slice
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title(title)
    
    # Convert plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url

def create_bar_chart(spam_count, ham_count):
    """
    Create a bar chart comparing spam and ham
    """
    categories = ['Ham', 'Spam']
    values = [ham_count, spam_count]
    colors = ['#28a745', '#dc3545']
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(categories, values, color=colors)
    plt.title('Spam vs Ham Message Count')
    plt.ylabel('Number of Messages')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url

def create_accuracy_chart(accuracy):
    """
    Create a gauge-like chart for accuracy
    """
    plt.figure(figsize=(6, 4))
    
    # Create a horizontal bar for accuracy
    colors = ['#dc3545', '#ffc107', '#28a745']
    plt.barh(['Accuracy'], [accuracy], color=colors[min(int(accuracy*3), 2)])
    plt.xlim(0, 1)
    plt.xlabel('Score')
    plt.title(f'Model Accuracy: {accuracy:.2%}')
    
    # Add percentage label
    plt.text(accuracy/2, 0, f'{accuracy:.1%}', 
             ha='center', va='center', color='white', fontweight='bold')
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url