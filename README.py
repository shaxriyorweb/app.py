<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Psixologik Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 10px;
        }
        h1, h2, h3 {
            color: #333;
        }
        .question {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-left: 20px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 15px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            border: 1px solid #ddd;
            background: #f9f9f9;
        }
    </style>
</head>
<body>

<h1>🧠 Psixologik Test</h1>

<div id="user-info">
    <h2>Ma'lumotlaringizni kiriting:</h2>
    <label>Ism: <input type="text" id="name" /></label>
    <label>Familiya: <input type="text" id="surname" /></label>
    <label>Yosh: <input type="number" id="age" min="7" max="25" /></label>
    <label>Jinsi:
        <select id="gender">
            <option value="">Tanlang</option>
            <option value="Erkak">Erkak</option>
            <option value="Ayol">Ayol</option>
        </select>
    </label>
    <label>Hudud:
        <select id="region">
            <option value="">Tanlang</option>
            <option>Toshkent</option>
            <option>Toshkent viloyati</option>
            <option>Andijon</option>
            <option>Farg‘ona</option>
            <option>Namangan</option>
            <option>Samarqand</option>
            <option>Buxoro</option>
            <option>Navoiy</option>
            <option>Xorazm</option>
            <option>Qashqadaryo</option>
            <option>Surxondaryo</option>
            <option>Jizzax</option>
        </select>
    </label>
    <button onclick="startTest()">Testni boshlash</button>
</div>

<div id="quiz" style="display:none;">
    <h2>📋 30 ta Savol</h2>
    <form id="quiz-form">
        <!-- Savollar bu yerga JS bilan qo‘yiladi -->
    </form>
    <button onclick="submitQuiz()">✅ Natijani ko‘rish</button>
</div>

<div id="result" class="result" style="display:none;">
    <h2>📊 Sizning Natijangiz</h2>
    <div id="result-text"></div>
    <div id="advice"></div>
</div>

<script>
    const questions = [
        ["Do‘stlaringiz bilan bo‘lishish siz uchun qanchalik muhim?", ["A. Juda muhim", "B. O‘rtacha", "C. Kamdan-kam"]],
        ["Yangi odamlar bilan tanishish sizga yoqadimi?", ["A. Ha, juda yoqadi", "B. Vaziyatga qarab", "C. Unchalik emas"]],
        ["Ishni yakunlash siz uchun qanchalik muhim?", ["A. Har doim tugataman", "B. Ba'zida tugataman", "C. Ko‘p holatda yarim yo‘lda qoldiraman"]],
        ["Stressli vaziyatlarda qanday harakat qilasiz?", ["A. Hissiyotimni ifodalayman", "B. Ichimga yutaman", "C. Maslahatlasha boshlayman"]],
        ["Yolg‘izlik sizga qanday ta’sir qiladi?", ["A. Tinchlik beradi", "B. Ko‘nikkanman", "C. Bezovta qiladi"]],
        ["Yangi topshiriqlarni bajarishda siz qanday harakat qilasiz?", ["A. Darhol kirishaman", "B. O‘ylab ko‘rib kirishaman", "C. Kechiktiraman"]],
        ["Do‘stlaringiz sizni qanday ta’riflaydi?", ["A. Ochiq va ijtimoiy", "B. Tinch va xotirjam", "C. Fikrlovchi va mustaqil"]],
        ["Muammoga duch kelsangiz, nima qilasiz?", ["A. Boshqalardan yordam so‘rayman", "B. Mustaqil hal qilaman", "C. Vaziyatga qarab"]],
        ["Dam olish kunlaringizni qanday o‘tkazasiz?", ["A. Do‘stlar bilan", "B. Oila davrasida", "C. Yolg‘iz kitob o‘qib"]],
        ["O‘zingizga bo‘lgan ishonchingiz qanchalik yuqori?", ["A. Yuqori", "B. O‘rtacha", "C. Kam"]],
        ["Hayotdagi maqsadingiz aniqmi?", ["A. Ha, juda aniq", "B. Taxminan bilaman", "C. Hali aniqlamadim"]],
        ["Yutuqlaringizni boshqalar bilan bo‘lishasizmi?", ["A. Ha", "B. Ba'zida", "C. Yo‘q"]],
        ["Tanqidni qanday qabul qilasiz?", ["A. Ijobiy", "B. Xafa bo‘laman", "C. E’tibor bermayman"]],
        ["Do‘stlaringiz soni qancha?", ["A. Juda ko‘p", "B. O‘rtacha", "C. Kam"]],
        ["Yangi ish boshlashdan oldin nima qilasiz?", ["A. Rejalashtiraman", "B. Darhol boshlayman", "C. O‘ylab yuraman"]],
        ["Stressni qanday yengasiz?", ["A. Sport bilan", "B. Suhbat orqali", "C. Yolg‘izlikda"]],
        ["Siz uchun muhim narsa nima?", ["A. Aloqalar", "B. Xavfsizlik", "C. Mustaqillik"]],
        ["Mas'uliyatli vazifalarda o‘zingizni qanday his qilasiz?", ["A. Ishonchli", "B. Biroz hayajon", "C. Qiyinchilik bilan"]],
        ["Ijtimoiy tadbirlarda siz...", ["A. Markazda bo‘laman", "B. Chekkada turaman", "C. Umuman qatnashmayman"]],
        ["O‘qish va o‘rganishga bo‘lgan munosabatingiz qanday?", ["A. Juda ijobiy", "B. Qiziqishga qarab", "C. Majburiyat sifatida"]],
        ["Muammoni boshqalarga aytish sizga osonmi?", ["A. Ha", "B. Vaziyatga qarab", "C. Yo‘q"]],
        ["O‘zingizni boshqalarga taqqoslaysizmi?", ["A. Kamdan-kam", "B. Ba'zida", "C. Tez-tez"]],
        ["Maqsad sari harakat qanday bo‘ladi?", ["A. Rejali", "B. Har xil", "C. Sekin"]],
        ["Ish jarayonida siz...", ["A. Hamma bilan ishlay olaman", "B. Tanlanganlar bilan", "C. Yolg‘iz yaxshi ishlayman"]],
        ["Qiyin vaziyatda siz...", ["A. Hal qilishga urinaman", "B. Qochaman", "C. Boshqalarga yuklayman"]],
        ["Sizning hayotiy qadriyatlaringiz...", ["A. Aniq va qat'iy", "B. Vaqtga qarab o‘zgaradi", "C. Hali shakllanmagan"]],
        ["Tashqi ko‘rinishingiz siz uchun...", ["A. Muhim", "B. Ortiqcha", "C. E’tibor bermayman"]],
        ["Tuyg‘ularingizni boshqarasizmi?", ["A. Ha", "B. Har doim emas", "C. Qiyin"]],
        ["Dushmanlik holatida...", ["A. Murosaga boraman", "B. Indamayman", "C. Qarshi chiqaman"]],
        ["Yangi g‘oyalarga ochiqmisiz?", ["A. Ha", "B. O‘ylab ko‘raman", "C. Shubha bilan qarayman"]]
    ];

    function startTest() {
        const name = document.getElementById('name').value.trim();
        const surname = document.getElementById('surname').value.trim();
        const age = parseInt(document.getElementById('age').value);
        const gender = document.getElementById('gender').value;
        const region = document.getElementById('region').value;

        if (!name || !surname || !age || !gender || !region) {
            alert("Iltimos, barcha ma’lumotlarni to‘liq kiriting.");
            return;
        }

        // Saqlab qo'yish uchun globalga
        window.userData = {name, surname, age, gender, region};

        document.getElementById('user-info').style.display = 'none';
        document.getElementById('quiz').style.display = 'block';

        // Savollarni tasodifiy aralashtirish
        shuffleArray(questions);

        const form = document.getElementById('quiz-form');
        form.innerHTML = '';
        questions.forEach((q, i) => {
            const div = document.createElement('div');
            div.className = 'question';
            div.innerHTML = `<p><strong>${i + 1}. ${q[0]}</strong></p>`;
            q[1].forEach(option => {
                const radio = document.createElement('input');
                radio.type = 'radio';
                radio.name = `q${i}`;
                radio.value = option.charAt(0);
                radio.id = `q${i}_${option.charAt(0)}`;

                const label = document.createElement('label');
                label.htmlFor = radio.id;
                label.textContent = option;

                div.appendChild(radio);
                div.appendChild(label);
            });
            form.appendChild(div);
        });
    }

    function submitQuiz() {
        const totalQuestions = questions.length;
        let aCount = 0, bCount = 0, cCount = 0;
        let answeredCount = 0;

        for (let i = 0; i < totalQuestions; i++) {
            const radios = document.getElementsByName(`q${i}`);
            let answered = false;
            for (const r of radios) {
                if (r.checked) {
                    answered = true;
                    answeredCount++;
                    if (r.value === 'A') aCount++;
                    else if (r.value === 'B') bCount++;
                    else if (r.value === 'C') cCount++;
                    break;
                }
            }
        }

        if (answeredCount === 0) {
            alert("Iltimos, hech bo‘lmaganda bitta savolga javob bering.");
            return;
        }

        const aPercent = ((aCount / answeredCount) * 100).toFixed(1);
        const bPercent = ((bCount / answeredCount) * 100).toFixed(1);
        const cPercent = ((cCount / answeredCount) * 100).toFixed(1);

        let advice = "";
        if (aCount > bCount && aCount > cCount) {
            advice = "Siz do‘stona, ochiq va ijtimoiy odamsiz.";
        } else if (bCount > aCount && bCount > cCount) {
            advice = "Siz diqqatli va mulohazali odamsiz.";
        } else if (cCount > aCount && cCount > bCount) {
            advice = "Siz mustaqil va ichki dunyoga ega odamsiz.";
        } else {
            advice = "Sizda turli fazilatlar uyg‘unlashgan. Bu yaxshi.";
        }

        const resultDiv = document.getElementById('result-text');
        const adviceDiv = document.getElementById('advice');

        resultDiv.innerHTML = `
            A javoblari: ${aCount} ta (${aPercent}%)<br/>
            B javoblari: ${bCount} ta (${bPercent}%)<br/>
            C javoblari: ${cCount} ta (${cPercent}%)<br/>
        `;
        adviceDiv.textContent = advice;

        document.getElementById('result').style.display = 'block';

        // Natijani localStorage yoki serverga yuborish uchun kod shu yerga qo‘yilishi mumkin
        console.log("Foydalanuvchi:", window.userData);
        console.log("Natija:", {aCount, bCount, cCount, aPercent, bPercent, cPercent});
    }

    function shuffleArray(array) {
        for (let i = array.length -1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
</script>

</body>
</html>
