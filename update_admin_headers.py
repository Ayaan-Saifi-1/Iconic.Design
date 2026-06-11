import os
import glob

files = glob.glob('c:/Users/Ayaan/Desktop/Iconic.Design/templates/admin*.html')

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the dark header with beige
    content = content.replace(
        '<div style="background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-darker) 100%); padding-top: 5rem; padding-bottom: 0;">',
        '<div style="background: rgba(235, 222, 202, 0.96); padding-top: 5rem; padding-bottom: 0;">'
    )
    
    # Text adjustments
    content = content.replace('text-white', 'text-dark')
    content = content.replace('background-color: rgba(255,255,255,0.1); color: white; border: 1px solid rgba(255,255,255,0.2);', 'background-color: rgba(0,0,0,0.05); color: var(--primary-dark); border: 1px solid rgba(0,0,0,0.1);')
    content = content.replace("onmouseover=\"this.style.backgroundColor='rgba(220, 53, 69, 0.9)'; this.style.borderColor='rgba(220, 53, 69, 0.9)'\"", "onmouseover=\"this.style.backgroundColor='rgba(220, 53, 69, 0.9)'; this.style.color='white';\"")
    content = content.replace("onmouseout=\"this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderColor='rgba(255,255,255,0.2)'\"", "onmouseout=\"this.style.backgroundColor='rgba(0,0,0,0.05)'; this.style.color='var(--primary-dark)';\"")
    
    # Nav borders and text
    content = content.replace('border-bottom: 1px solid rgba(255,255,255,0.1);', 'border-bottom: 1px solid rgba(0,0,0,0.1);')
    content = content.replace("onmouseover=\"this.style.color='#fff'\" onmouseout=\"this.style.color='#94a3b8'\"", "onmouseover=\"this.style.color='var(--primary-dark)'\" onmouseout=\"this.style.color='rgba(15,30,60,0.6)'\"")
    content = content.replace("color:#94a3b8;", "color:rgba(15,30,60,0.6);")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
        
print("Updated admin files.")
