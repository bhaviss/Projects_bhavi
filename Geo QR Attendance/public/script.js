const classroomCoords = { lat: 53.5603759, lon: -113.4456192 };  // Classroom coordinates
        const allowedRadius = 8;  // Allowed radius in meters
        function getLoc() {
            if (!navigator.geolocation) {
                document.getElementById('locationDisplay').innerText = "Geolocation is not supported by your browser.";
                return;
            }

            document.getElementById('locationDisplay').innerText = "Fetching your location...";          
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const userLat = position.coords.latitude;
                    const userLon = position.coords.longitude;
                    const distance = calculateDistance(classroomCoords.lat, classroomCoords.lon, userLat, userLon);

                    if (distance <= allowedRadius) {
                        document.getElementById('locationDisplay').innerText = `Location: Within allowed area (${Math.round(distance)} meters away)`;
                        document.getElementById('message').innerText = "";
                    } else {
                        document.getElementById('locationDisplay').innerText = `Location: Outside allowed area (${Math.round(distance)} meters away)`;
                        document.getElementById('message').innerText = "You must be in the classroom area to mark attendance.";
                    }
                },
                (error) => {
                    document.getElementById('locationDisplay').innerText = "Unable to fetch location.";
                    console.error("Error getting geolocation: ", error);
                }
            );
        }

        function calculateDistance(lat1, lon1, lat2, lon2) {
            const R = 6371;  // Radius of the Earth in km
            const dLat = deg2rad(lat2 - lat1);
            const dLon = deg2rad(lon2 - lon1);
            const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                      Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
                      Math.sin(dLon / 2) * Math.sin(dLon / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            return R * c * 1000;  // Convert to meters
        }

        function deg2rad(deg) {
            return deg * (Math.PI / 180);
        }

        function handleSubmit(event) {
    event.preventDefault();

    const Name = document.getElementById('name').value;
    const Email = document.getElementById('email').value;
    const ClassName = document.getElementById('className').value;
    const location = document.getElementById('locationDisplay').innerText; // Fetch location displayed on the page

    if (document.getElementById('message').innerText === "") {  // Check if there's no error message
        fetch('https://projectitm.onrender.com/api/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ Name, Email, ClassName, location }), 
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('message').innerText = data.message;
            window.location.href = "success.html"; 
        })
        .catch(error => {
            console.error('Error submitting form:', error);
            document.getElementById('message').innerText = "Submission failed. Please try again later.";
        });
    } else {
        document.getElementById('message').innerText = "Submission failed because you are outside the allowed area. Please return to the classroom.";
    }
}
        document.getElementById('dataForm').addEventListener('submit', handleSubmit);

        // Fetch location on page load
        getLoc();
 
