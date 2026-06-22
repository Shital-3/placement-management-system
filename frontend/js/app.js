const API_URL = "http://127.0.0.1:8000";

// ================= TOKEN =================
function saveToken(token) {
    localStorage.setItem("token", token);
}

function getToken() {
    return localStorage.getItem("token");
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

// ================= LOGIN =================
async function loginUser(event) {
    event.preventDefault();

    const email = document.getElementById("email")?.value;
    const password = document.getElementById("password")?.value;

    if (!email || !password) {
        alert("Please fill all fields");
        return;
    }

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
        const res = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.detail || "Login failed");
            return;
        }

        saveToken(data.access_token);
        redirectDashboard(data.role);

    } catch (err) {
        console.error(err);
        alert("Server error");
    }
}

// ================= REDIRECT =================
function redirectDashboard(role) {
    if (role === "admin") {
        window.location.href = "admin-dashboard.html";
    } else if (role === "student") {
        window.location.href = "student-dashboard.html";
    } else if (role === "alumni") {
        window.location.href = "alumni-dashboard.html";
    } else {
        alert("Unknown role");
    }
}

// ================= REGISTER =================
window.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const name = document.getElementById("name")?.value;
            const email = document.getElementById("registerEmail")?.value;
            const password = document.getElementById("registerPassword")?.value;

            if (!name || !email || !password) {
                alert("All fields required!");
                return;
            }

            try {
                const res = await fetch(`${API_URL}/register`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        name,
                        email,
                        password,
                        role: "student"
                    })
                });

                const data = await res.json();

                if (res.ok) {
                    alert("Registration successful!");
                } else {
                    alert(data.detail || "Registration failed");
                }

            } catch (err) {
                console.error(err);
                alert("Server error");
            }
        });
    }
});

// ================= ADMIN DASHBOARD =================
async function loadDashboard() {
    try {
        const token = getToken();

        const res = await fetch(`${API_URL}/admin/dashboard`, {
            headers: {
                Authorization: "Bearer " + token
            }
        });

        if (!res.ok) {
            console.error("Dashboard load failed");
            return;
        }

        const data = await res.json();

        const students = document.getElementById("students");
        const jobs = document.getElementById("jobs");
        const applications = document.getElementById("applications");

        if (students) students.innerText = data.total_students;
        if (jobs) jobs.innerText = data.total_jobs;
        if (applications) applications.innerText = data.total_applications;

    } catch (err) {
        console.error(err);
    }
}

// ================= LOAD APPLICATIONS =================
async function loadApplications() {
    try {
        const token = getToken();

        const res = await fetch(`${API_URL}/admin/applications`, {
            headers: {
                Authorization: "Bearer " + token
            }
        });

        const data = await res.json();

        const table = document.querySelector("#applicationsTable tbody");

        if (!table) return;

        table.innerHTML = "";

        if (!Array.isArray(data) || data.length === 0) {
            table.innerHTML = "<tr><td colspan='5'>No applications found</td></tr>";
            return;
        }

        data.forEach(app => {
            table.innerHTML += `
                <tr>
                    <td>${app.id}</td>
                    <td>${app.student_name}</td>
                    <td>${app.job_title}</td>
                    <td>${app.status}</td>
                    <td>
                        <button onclick="updateStatus(${app.id}, 'approved')">Approve</button>
                        <button onclick="updateStatus(${app.id}, 'rejected')">Reject</button>
                    </td>
                </tr>
            `;
        });

    } catch (err) {
        console.error(err);
    }
}

// ================= UPDATE STATUS =================
async function updateStatus(id, status) {
    try {
        const token = getToken();

        const res = await fetch(`${API_URL}/admin/update-status/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token
            },
            body: JSON.stringify({ status })
        });

        if (!res.ok) {
            const data = await res.json();
            alert(data.detail || "Update failed");
            return;
        }

        alert("Updated successfully!");
        loadApplications();

    } catch (err) {
        console.error(err);
        alert("Server error");
    }
}