// var image=[
//     '../img/background1.jpg',
//     '../img/background2.jpg',
//     '../img/background3.jpg',
// ];

// var currentid = 0;
// var myelement = document.getElementsById('slide');

// setInterval(function() {
//     currentid = (currentid + 1) % image.length; // Chuyển đến ảnh tiếp theo
//     myelement.style.backgroundImage = 'url(' + image[currentid] + ')'; // Cập nhật ảnh nền
//   }, 1000);

//   #myDiv {
//     width: 500px;
//     height: 500px;
//     background-image: url('image1.jpg');
//     animation-name: changeImage;
//     animation-duration: 10s;
//     animation-iteration-count: infinite;
//   }
  
  // @keyframes changeImage {
  //   0% { background-image: url('image1.jpg'); }
  //   25% { background-image: url('image2.jpg'); }
  //   50% { background-image: url('image3.jpg'); }
  //   75% { background-image: url('image4.jpg'); }
  //   100% { background-image: url('image1.jpg'); }
  // }




// var images = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg'];
// var currentImageIndex = 0;
// var myDiv = document.getElementById('myDiv');

// setInterval(function() {
//   currentImageIndex++;
//   if (currentImageIndex >= images.length) {
//     currentImageIndex = 0;
//   }
//   myDiv.style.backgroundImage = 'url(' + images[currentImageIndex] + ')';
// }, 5000);