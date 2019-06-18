package com.example.smartwateringsystem;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.content.Intent;



public class loginx extends AppCompatActivity {

    private EditText username;

    private Button Login;
    private int counter = 5;
    private EditText password;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loginx);


        password = (EditText) findViewById(R.id.Fpass);
        Login = (Button) findViewById(R.id.Blogin);
        username = (EditText) findViewById(R.id.Fuser);

        Login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                validate(username.getText().toString(), password.getText().toString());
            }
        });

    }


    public void validate(String userName, String userPass) {
       // if ((userName == "goutham") && (userPass == "1234")) {
            Intent i = new Intent(loginx.this, ValveC.class);
            startActivity(i);
        //} else {
          //  counter--;
           // if (counter == 0) {
           //     Login.setEnabled(false);
            }
        }








