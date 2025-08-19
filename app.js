import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getFirestore, collection, query, where, getDocs } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

// 🔐 Tu configuración de Firebase
const firebaseConfig = {
      apiKey: "AIzaSyA4t1dJ1Lmkc02SzShxczQzwhGAfFIKg6I",
      authDomain: "asistente-ister.firebaseapp.com",
      projectId: "asistente-ister",
      storageBucket: "asistente-ister.firebasestorage.app",
      messagingSenderId: "865101154570",
      appId: "1:865101154570:web:018dedb60bb2f5b565d2f3",
      measurementId: "G-64GG5BCJ14"
    };

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const searchBtn = document.getElementById("searchBtn");
const searchInput = document.getElementById("searchInput");
const resultTable = document.getElementById("resultTable");

searchBtn.addEventListener("click", async () => {
  const valor = searchInput.value.trim();
  resultTable.innerHTML = "";

  if (valor === "") return;

  const registrosRef = collection(db, "registros");

  // Solo consultar por cédula
  const q = query(registrosRef, where("cedula", "==", valor));
  const snap = await getDocs(q);

  if (snap.empty) {
    resultTable.innerHTML = "<tr><td colspan='5'>No se encontraron resultados</td></tr>";
    return;
  }

  snap.forEach(doc => {
    const d = doc.data();
    resultTable.innerHTML += `
      <tr>
        <td>${d.nombre}</td>
        <td>${d.uid}</td>
        <td>${d.fecha}</td>
        <td>${d.hora_entrada}</td>
        <td>${d.hora_salida}</td>
      </tr>`;
  });
});
