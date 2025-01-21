// Fetch students and display them
function fetchStudents() {
    fetch('/students')
    .then(response => response.json())
    .then(data => {
        let studentTableBody = document.getElementById('student-table-body');
        studentTableBody.innerHTML = '';
        if (data.length === 0) {
            studentTableBody.innerHTML = '<tr><td colspan="4">No students found.</td></tr>';
        } else {
            data.forEach(student => {
                let row = `
                    <tr>
                        <td>${student.name}</td>
                        <td>${student.roll_number}</td>
                        <td>${student.subject_name}</td>
                        <td>${student.grade}</td>
                    </tr>
                `;
                studentTableBody.innerHTML += row;
            });
        }
    })
    .catch(error => {
        console.error('Error fetching students:', error);
        alert('Error fetching students data.');
    });
}

// Fetch staff and display them
function fetchStaff() {
    fetch('/staff')
    .then(response => response.json())
    .then(data => {
        let staffTableBody = document.getElementById('staff-table-body');
        staffTableBody.innerHTML = '';
        if (data.length === 0) {
            staffTableBody.innerHTML = '<tr><td colspan="3">No staff found.</td></tr>';
        } else {
            data.forEach(staff => {
                let row = `
                    <tr>
                        <td>${staff.name}</td>
                        <td>${staff.position}</td>
                        <td>${staff.contact_number}</td>
                    </tr>
                `;
                staffTableBody.innerHTML += row;
            });
        }
    })
    .catch(error => {
        console.error('Error fetching staff:', error);
        alert('Error fetching staff data.');
    });
}

// Filter students by name
function filterStudents() {
    let filter = document.getElementById('student-search').value;
    fetch(`/students?name=${filter}`)
        .then(response => response.json())
        .then(data => {
            let studentTableBody = document.getElementById('student-table-body');
            studentTableBody.innerHTML = '';
            if (data.length === 0) {
                studentTableBody.innerHTML = '<tr><td colspan="4">No results found.</td></tr>';
            } else {
                data.forEach(student => {
                    let row = `
                        <tr>
                            <td>${student.name}</td>
                            <td>${student.roll_number}</td>
                            <td>${student.subject_name}</td>
                            <td>${student.grade}</td>
                        </tr>
                    `;
                    studentTableBody.innerHTML += row;
                });
            }
        })
        .catch(error => {
            console.error('Error filtering students:', error);
            alert('Error filtering students.');
        });
}

// Filter staff by name
function filterStaff() {
    let filter = document.getElementById('staff-search').value;
    fetch(`/staff?name=${filter}`)
        .then(response => response.json())
        .then(data => {
            let staffTableBody = document.getElementById('staff-table-body');
            staffTableBody.innerHTML = '';
            if (data.length === 0) {
                staffTableBody.innerHTML = '<tr><td colspan="3">No results found.</td></tr>';
            } else {
                data.forEach(staff => {
                    let row = `
                        <tr>
                            <td>${staff.name}</td>
                            <td>${staff.position}</td>
                            <td>${staff.contact_number}</td>
                        </tr>
                    `;
                    staffTableBody.innerHTML += row;
                });
            }
        })
        .catch(error => {
            console.error('Error filtering staff:', error);
            alert('Error filtering staff.');
        });
}

// Add a new student
function addStudent(event) {
    event.preventDefault();
    
    let name = document.getElementById('student-name').value;
    let roll_number = document.getElementById('student-roll-number').value;
    let subject_name = document.getElementById('student-subject').value;
    let grade = document.getElementById('student-grade').value;
    
    fetch('/add_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `name=${name}&roll_number=${roll_number}&subject_name=${subject_name}&grade=${grade}`
    })
    .then(response => response.json())
    .then(() => {
        fetchStudents(); // Refresh the student list
        alert('Student added successfully!');
    })
    .catch(error => {
        console.error('Error adding student:', error);
        alert('Error adding student.');
    });
}

// Add a new staff member
function addStaff(event) {
    event.preventDefault();
    
    let name = document.getElementById('staff-name').value;
    let position = document.getElementById('staff-position').value;
    let contact_number = document.getElementById('staff-contact').value;
    
    fetch('/add_staff', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `name=${name}&position=${position}&contact_number=${contact_number}`
    })
    .then(response => response.json())
    .then(() => {
        fetchStaff(); // Refresh the staff list
        alert('Staff added successfully!');
    })
    .catch(error => {
        console.error('Error adding staff:', error);
        alert('Error adding staff.');
    });
}

// Add a new meal plan
function addMealPlan(event) {
    event.preventDefault();
    
    let student_id = document.getElementById('meal-plan-student-id').value;
    let meal_plan = document.getElementById('meal-plan').value;
    
    fetch('/add_meal_plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `student_id=${student_id}&meal_plan=${meal_plan}`
    })
    .then(response => response.json())
    .then(() => {
        alert('Meal plan added successfully!');
    })
    .catch(error => {
        console.error('Error adding meal plan:', error);
        alert('Error adding meal plan.');
    });
}

// Initial fetch on page load
document.addEventListener("DOMContentLoaded", () => {
    fetchStudents();
    fetchStaff();
    
    // Event listeners for form submissions
    document.getElementById('add-student-form').addEventListener('submit', addStudent);
    document.getElementById('add-staff-form').addEventListener('submit', addStaff);
    document.getElementById('add-meal-plan-form').addEventListener('submit', addMealPlan);
});
