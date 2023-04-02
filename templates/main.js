const previewImage= (event)=>{
    const imgfiles=event.target.files;
    const imageSrc=URL.createObjectURL(imgfiles[0]);
    const imagePreviewElement=document.querySelector("#preview-selected-image");
    
    imagePreviewElement.src=imageSrc;
}