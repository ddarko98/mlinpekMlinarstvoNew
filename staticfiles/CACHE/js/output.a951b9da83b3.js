window.onload=function(){var videos=document.querySelectorAll('video');videos.forEach(function(video){video.muted=true;video.play().then(()=>{console.log('Video is playing automatically');}).catch(function(error){console.log('Autoplay prevented: ',error);});});};;