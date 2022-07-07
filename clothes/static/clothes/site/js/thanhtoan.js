const exampleRadios2 = document.getElementById('exampleRadios2')
const thanhToanNganHang = document.getElementById('thanhToanNganHang')
const exampleRadios1 =document.getElementById('exampleRadios1')
exampleRadios2.addEventListener('click',()=>{
    thanhToanNganHang.style.display= "block"
})
exampleRadios1.addEventListener('click',()=>{
    cod()
})

function cod() {
  thanhToanNganHang.style.display= "none"
}
// js phan tang giam so luong sp
const tang= document.getElementById('tang')
const giam= document.getElementById('giam')
const soluong = document.getElementById('soluong')
let value =1;
tang.addEventListener("click",()=>{
    value++
    giam.disabled=false
    giam.classList.remove('none')
    soluong.innerText = value
})
giam.addEventListener("click",()=>{
    value--
    if(value==0){
      giam.disabled= true
      giam.classList.add("none")
    }
    soluong.innerText = value
})
