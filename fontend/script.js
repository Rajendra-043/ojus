// Standalone frontend. Tries Django API at http://127.0.0.1:8000, falls back to built-in data.
const API = "http://127.0.0.1:8000";
const FALLBACK = {
  events: [["Robotics","Build robots and solve challenges."],["Programming","Coding and programming contests."],["Gaming","Gaming tournaments and challenges."],["Circuit Design","Test your electronics skills."],["Singing","Music and live performances."],["Dancing","Solo, group and freestyle dance."],["Craft & Art","Painting, drawing and creativity."],["Sports","Cricket, football, badminton and more."],["Paper Presentation","Present innovative ideas."]],
  clubs: [["Vista","Culture"],["Innovation","Ideas"],["Ekaksh","Drama"],["Laasya","Dance"],["Alankar","Music"],["Speaking Club","Communication"],["Astro","Astronomy"],["Clicks","Photography"],["Techno","Technology"],["Robotics","Robotics"],["Quizbizz","Quiz"],["PAC","Activities"],["GDSC","Development"],["Startup","Business"],["Literary","Writing"]],
  schedule: [["Day 1","Opening","Technical Events","Gaming"],["Day 2","Workshops","Cultural Events","Sports"],["Day 3","Finals","Prize Distribution","Closing"]],
  gallery: ["Music","Dance","Robotics","Technology","Art","Gaming","Awards","Memories"],
  winners: [["Rhythm Crew","Dance Winner"],["Team Nova","Technical Winner"],["Pixel Warriors","Gaming Winner"]],
  updates: [["Registration Open","Register for your favourite events."],["New Competitions","Explore new challenges."],["Special Shows","Enjoy performances and activities."]],
  help: [["Registration Help","Help with registration and forms."],["Venue Help","Find your event venue easily."],["Technical Support","Help with technical problems."],["Volunteer Help","Volunteers can guide you."],["Emergency Help","Contact coordinators for urgent help."],["General Enquiry","Ask the Help Desk for any query."]],
  faqs: [["Who can participate?","Students can participate according to event rules."],["Can I join multiple events?","Yes, depending on the event schedule."],["How can I register?","Fill the registration form below."],["Where are events held?","At different venues inside BIT Durg."],["What if I have a problem?","Visit the OJAS Help Desk or contact volunteers."]]
};
async function get(path, key) {
  try {
    const r = await fetch(API + path);
    if (!r.ok) throw 0;
    const j = await r.json();
    const vals = j[key] || j[Object.keys(j)[0]];
    if (vals && vals.length) return vals;
    throw 0;
  } catch { return null; }
}
function esc(s){return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]))}
document.addEventListener("DOMContentLoaded", async () => {
  let events = await get("/api/events/","events") || FALLBACK.events.map(([name,description])=>({name,description}));
  document.getElementById("events-grid").innerHTML = events.map(e=>`<div class="event"><b>🎯</b><h3>${esc(e.name||e[0])}</h3><p>${esc(e.description||e[1]||"")}</p></div>`).join("");
  let clubs = await get("/api/clubs/","clubs") || FALLBACK.clubs.map(([name,category])=>({name,category}));
  document.getElementById("clubs-grid").innerHTML = clubs.map(c=>`<div class="club"><b>🤝</b><h3>${esc(c.name||c[0])}</h3><p>${esc(c.category||c[1]||"")}</p></div>`).join("");
  let sch = await get("/api/schedule/","schedule") || FALLBACK.schedule.map(([day,morning,afternoon,evening])=>({day,morning,afternoon,evening}));
  const tbl = document.getElementById("schedule-table");
  sch.forEach(s=>{const tr=document.createElement("tr");tr.innerHTML=`<td>${esc(s.day||s[0])}</td><td>${esc(s.morning||s[1])}</td><td>${esc(s.afternoon||s[2])}</td><td>${esc(s.evening||s[3])}</td>`;tbl.appendChild(tr);});
  const gal = FALLBACK.gallery;
  document.getElementById("gallery-grid").innerHTML = gal.map(t=>`<div class="photo">\u25a0<span>${esc(t)}</span></div>`).join("");
  document.getElementById("winners-grid").innerHTML = FALLBACK.winners.map(([t,c])=>`<div class="winner"><h3>\u25a0 ${esc(t)}</h3><p>${esc(c)}</p></div>`).join("");
  let upd = await get("/api/updates/","updates") || FALLBACK.updates.map(([title,description])=>({title,description}));
  document.getElementById("updates-grid").innerHTML = upd.map(u=>`<div class="card"><h3>\u25a0 ${esc(u.title||u[0])}</h3><p>${esc(u.description||u[1]||"")}</p></div>`).join("");
  document.getElementById("help-grid").innerHTML = FALLBACK.help.map(([t,d])=>`<div class="help"><b>\u25a0</b><h3>${esc(t)}</h3><p>${esc(d)}</p></div>`).join("");
  let faqs = await get("/api/faqs/","faqs") || FALLBACK.faqs.map(([question,answer])=>({question,answer}));
  document.getElementById("faq-list").innerHTML = faqs.map(f=>`<div class="question"><h3>${esc(f.question||f[0])}</h3><p>${esc(f.answer||f[1]||"")}</p></div>`).join("");
  for (const [id,url,ok] of [["register-form","/api/register/","Registered! See you at OJAS 2026."],["feedback-form","/api/feedback/","Thanks for your feedback!"]]) {
    const form = document.getElementById(id);
    form.addEventListener("submit", async (e)=>{
      e.preventDefault();
      const payload = Object.fromEntries(new FormData(form).entries());
      const note = document.createElement("div"); note.className="msg"; note.textContent="Sending..."; form.prepend(note);
      try {
        const r = await fetch(API+url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
        const j = await r.json();
        note.textContent = j.ok ? ok : "Backend not running — start Django (see README). Your data was NOT saved.";
        if (j.ok) form.reset();
      } catch { note.textContent = "Backend not running — start Django on :8000 (see README)."; }
    });
  }
});
