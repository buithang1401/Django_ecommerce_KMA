const dropitems = document.getElementById('gg-shopping-cart')
const carditem = document.getElementById('cart-if-items')

let i=1
dropitems.addEventListener('mousemove',()=>{
  thaydoi()
})


function thaydoi(){
  if(i==1){
    carditem.style="display: block"
    i--
  }
  else{
    carditem.style="display: none"
    i=1
  }
}
