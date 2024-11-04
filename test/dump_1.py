
import os

def one():
    ax = [1,2,3,4,5]
    ay = [1,3,4,6,9]

    min_width , max_width = min(ax) - prozentwert(min(ax), 5), max(ax) + prozentwert(max(ax), 5)
    min_height, max_height = min(ay) - prozentwert(min(ay),5), max(ay) + prozentwert(max(ay),5)

    print(min_width, max_width, min_height, max_height)
def prozentwert(gesamtwert, prozentsatz):
    return (gesamtwert * prozentsatz) / 100

def two():
    keys = ['Website ID', 'Overall Category', 'First Contentful Paint Time', 'First Contentful Paint Score', 'Largest Contentful Paint Time', 'Largest Contentful PaintCP Score', 'Total Blocking Time', 'Cumulative Layout Shift Time', 'Cumulative Layout Shift Score', 'Layout Shifts', 'Speed Index', 'Time to Interactive', 'DOM Size', 'Offscreen Images', 'Total Byte Weight', 'Baymard Score', 'Anzahl a Tags', 'Anzahl p Tags', 'Anzahl div Tags', 'Anzahl IMG Tags', 'Anzahl Button Tags']
    for key in keys:
        ordner_pfad = f'/Users/HugoWienhold/Desktop/Graphen/Circle with Regression/{key}'
        os.makedirs(ordner_pfad, exist_ok=True)

two()