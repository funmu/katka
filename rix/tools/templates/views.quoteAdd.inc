<!-- ****** ADD QUOTE FORM ****** -->

<!-- Special version of Bootstrap that only affects content wrapped in .bootstrap-iso -->
<link rel="stylesheet" href="https://formden.com/static/cdn/bootstrap-iso.css" /> 

<!-- Inline CSS based on choices in "Settings" tab -->
<style>
 .bootstrap-iso { background-color: green}
 .bootstrap-iso .formden_header h2, 
 .bootstrap-iso .formden_header p, 
 .bootstrap-iso form 
  {font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif; color: #1de511}

 .bootstrap-iso form button, 
 .bootstrap-iso form button:hover
 {color: #ffffff !important;} 
 
 .asteriskField{color: red;}
 </style>

<!-- HTML Form (wrapped in a .bootstrap-iso div) -->
<div class="bootstrap-iso">
 <div class="container-fluid">
  <div class="row">
   <div class="col-md-12 col-sm-12 col-xs-12">
    <form method="post" action="/quote/add">
     <div class="form-group ">
      <label class="control-label requiredField" for="message">
       Quote
       <span class="asteriskField">
        *
       </span>
      </label>
      <textarea class="form-control" cols="40" id="message" name="message" placeholder="Life is Beautiful ..." rows="4"></textarea>
     </div>
     <div class="form-group ">
      <label class="control-label requiredField" for="author">
       Author
       <span class="asteriskField">
        *
       </span>
      </label>
      <input class="form-control" id="author" name="author" placeholder="Anonymous" type="text"/>
     </div>
     <div class="form-group">
      <div>
       <button class="btn btn-warning " name="submit" type="submit">
        Add Quote
       </button>
      </div>
     </div>
    </form>
   </div>
  </div>
 </div>
</div>
