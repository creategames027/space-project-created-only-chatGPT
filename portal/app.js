const objects = [
  {name:'Sun', type:'Star', section:'Known'},
  {name:'Andromeda Galaxy', type:'Galaxy', section:'Known'},
  {name:'Fast Radio Bursts', type:'Phenomenon', section:'New Discovery'},
  {name:'TON 618', type:'Black Hole', section:'Known'}
];

function searchObjects(){
 const input=document.getElementById('search').value.toLowerCase();
 const result=document.getElementById('result');
 const found=objects.filter(o=>o.name.toLowerCase().includes(input));
 result.innerHTML=found.map(o=>`<p>🌌 ${o.name} — ${o.type} (${o.section})</p>`).join('') || 'Nothing found';
}
