    <!-- ******LOGIN FORM****** -->
    <div class="jumbotron text-center form-cover">
        <h1><span class="fa fa-lock"></span> {TEMPLATE_APP_NAME_GOES_HERE}</h1>

        <div class="row">
        	<div class="col-sm-3">
		        <h3>Login Using Services</h3>
		    </div>
		    <div class="col-sm-3">
		        <a href="/auth/google" class="btn btn-danger btn-large">
		            <span class="fa fa-google-plus"></span> Google</a>
		    </div>
		</div>

        <hr/>
        <div class="row">
        	<div class="col-sm-3">
		        <h3>Login Locally</h3>
		    </div>
		    <div class="col-sm-6">
                <form action="/login" method="post">
                    <div class="form-group">
                        <label>Email</label>
                        <input type="text" class="form-control" name="email">
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" class="form-control" name="password">
                    </div>

                    <button type="submit" class="btn btn-warning btn-lg">Login</button>
                </form>		    	
		    </div>
        </div>
<!--
        <a href="/login_local" class="btn btn-default"><span class="fa fa-user"></span> Local Login</a>
-->
        <hr/>
        <div class="row">
	        <p>Register with: 
		        <a href="/signup" class="btn btn-default"><span class="fa fa-user"></span> Local Signup</a>
	        </p>
	    </div>
    </div>
