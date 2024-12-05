import pandas as pd
import folium
from folium.plugins import HeatMap

# Expanded dataset
data = pd.DataFrame({
    'latitude': [28.6139, 19.0760, 13.0827, 22.5726, 12.9716, 
                 26.9124, 23.0225, 17.3850, 21.1458, 15.2993],
    'longitude': [77.2090, 72.8777, 80.2707, 88.3639, 77.5946, 
                  75.7873, 72.5714, 78.4867, 79.0882, 74.1240],
    'location': ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore', 
                 'Jaipur', 'Ahmedabad', 'Hyderabad', 'Nagpur', 'Goa'],
    'disease': ['Heart Disease', 'Respiratory Issues', 'Cancer', 'Malaria', 'Diabetes', 
                'Tuberculosis', 'Heart Disease', 'Dengue', 'Cancer', 'Malaria'],
    'occurrences': [5000, 3000, 2000, 1000, 1500, 1200, 4000, 800, 1800, 600],
    'death_rate': [25, 15, 18, 5, 10, 8, 20, 3, 12, 4]
})

# Initialize the map centered on India
india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Prepare data for HeatMap
heat_data = [
    [row['latitude'], row['longitude'], row['occurrences']] for _, row in data.iterrows()
]

# Add HeatMap layer
HeatMap(heat_data, radius=15).add_to(india_map)

# Add markers for specific details
for _, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=(
            f"Location: {row['location']}<br>"
            f"Disease: {row['disease']}<br>"
            f"Occurrences: {row['occurrences']}<br>"
            f"Death Rate: {row['death_rate']}%"
        ),
    ).add_to(india_map)

# Save the map to an HTML file
india_map.save("expanded_india_disease_heatmap.html")

print("Heatmap saved as 'expanded_india_disease_heatmap.html'")
