from pathlib import Path 
p=Path('package.json') 
d=p.read_text() 
d=d.replace('" "expo: 48.0.18','expo: 56.0.3') 
p.write_text(d) 
