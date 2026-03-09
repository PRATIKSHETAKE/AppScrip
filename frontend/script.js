async function analyze(){

const sector = document.getElementById("sector").value
const resultBox = document.getElementById("result")
const loading = document.getElementById("loading")

resultBox.innerHTML=""
loading.style.display="block"

try{

const tokenResponse = await fetch("http://127.0.0.1:8000/guest")

const tokenData = await tokenResponse.json()

const token = tokenData.access_token

const response = await fetch(`http://127.0.0.1:8000/analyze/${sector}`,{
headers:{
"Authorization":`Bearer ${token}`
}
})

const data = await response.json()

loading.style.display="none"

resultBox.innerHTML = `
<div class="card p-3">
<h4>Market Analysis</h4>
<pre>${data.report_markdown}</pre>
</div>
`

}catch(error){

loading.style.display="none"

resultBox.innerHTML = `
<div class="alert alert-danger">
Error generating analysis
</div>
`

}
}