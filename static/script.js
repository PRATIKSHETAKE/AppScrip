async function analyze(){

const sector = document.getElementById("sector").value

const resultBox = document.getElementById("result")

const loading = document.getElementById("loading")

loading.style.display="block"
resultBox.innerHTML=""

try{

const tokenResponse = await fetch("/guest")
const tokenData = await tokenResponse.json()

const token = tokenData.access_token

const response = await fetch(`/analyze/${sector}`,{
headers:{
"Authorization":`Bearer ${token}`
}
})

const data = await response.json()

loading.style.display="none"

const html = marked.parse(data.report_markdown)

resultBox.innerHTML = `
<div class="card p-3">
${html}
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
