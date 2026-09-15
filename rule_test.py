import sys
sys.path.insert(0, 'src')

from utils import classify_status

print(f"temp=28, humidity=40(should be normal): {classify_status(28, 40)}")
print(f"temp=32, humidity=40(should be normal): {classify_status(32, 40)}")
print(f"temp=32, humidity=80(should be warning): {classify_status(32, 80)}")

