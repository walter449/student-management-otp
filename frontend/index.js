const API_URL = "/students";

document.addEventListener("DOMContentLoaded", () => {
    setupForm();
    loadStudents();
});

function setupForm() {
    const form = document.getElementById("student-form");
    const cancelBtn = document.getElementById("cancel-btn");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        saveStudent();
    });

    cancelBtn.addEventListener("click", () => {
        clearForm();
    });
}

function saveStudent() {
    const id = document.getElementById("student-id").value;
    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const grade = document.getElementById("grade").value;

    const studentData = { name, age, grade };

    const method = id ? "PUT" : "POST";
    const url = id ? `${API_URL}/${id}` : API_URL;

    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(studentData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error en la operación");
        }

        return response.json();
    })
    .then(data => {
        alert("Estudiante guardado correctamente");

        clearForm();
        loadStudents();
    })
    .catch(error => {
        alert(error.message);
    });
}

function loadStudents() {
    fetch(API_URL)
        .then(response => response.json())
        .then(data => {
            const studentList = document.getElementById("student-list");

            studentList.innerHTML = "";

            data.forEach(student => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${student.id}</td>
                    <td>${student.name}</td>
                    <td>${student.grade}</td>
                    <td>
                        <button onclick="editStudent(${student.id}, '${student.name}', ${student.age}, ${student.grade})">
                            Editar
                        </button>

                        <button onclick="deleteStudent(${student.id})">
                            Eliminar
                        </button>
                    </td>
                `;

                studentList.appendChild(row);
            });
        });
}

function editStudent(id, name, age, grade) {
    document.getElementById("student-id").value = id;
    document.getElementById("name").value = name;
    document.getElementById("age").value = age;
    document.getElementById("grade").value = grade;
}

function deleteStudent(id) {
    if (!confirm("¿Seguro que deseas eliminar este estudiante?")) {
        return;
    }

    fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error al eliminar");
        }

        loadStudents();
    })
    .catch(error => {
        alert(error.message);
    });
}

function clearForm() {
    document.getElementById("student-form").reset();
    document.getElementById("student-id").value = "";
}
