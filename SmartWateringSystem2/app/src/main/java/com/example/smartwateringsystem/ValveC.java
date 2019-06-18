package com.example.smartwateringsystem;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.app.Activity;


public class ValveC extends Activity {
    public static final String PARAM = "Param";
    public static final String PARAM1 = "Param1";
    private Button data;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_valve_c);

        data = (Button) findViewById(R.id.Bdata);
        data.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(ValveC.this, database.class);
                i.putExtra(PARAM, " Displaying sensor data");
                startActivity(i);

            }

        });

        data = (Button) findViewById(R.id.Adata);
        data.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(ValveC.this, database1.class);
                i.putExtra(PARAM1, " Displaying sensor data");
                startActivity(i);

            }

        });

    }
}