package com.simats.brainbattle

import android.content.Intent
import android.os.Bundle
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton
import com.simats.brainbattle.api.*

import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class SignupActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_signup)

        val username = findViewById<EditText>(R.id.etUsername)
        val email = findViewById<EditText>(R.id.etEmail)
        val password = findViewById<EditText>(R.id.etPassword)

        val btnSignup = findViewById<MaterialButton>(R.id.btnSignup)
        val loginText = findViewById<TextView>(R.id.loginText)

        // ✅ Signup button
        btnSignup.setOnClickListener {

            val nameText = username.text.toString().trim()
            val emailText = email.text.toString().trim()
            val passText = password.text.toString().trim()

            if (nameText.isEmpty() || emailText.isEmpty() || passText.isEmpty()) {
                Toast.makeText(this, "Fill all fields", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val request = AuthRequest(
                username = nameText,
                email = emailText,
                password = passText
            )

            ApiClient.instance.signup(request)
                .enqueue(object : Callback<SimpleResponse> {

                    override fun onResponse(
                        call: Call<SimpleResponse>,
                        response: Response<SimpleResponse>
                    ) {

                        if (response.isSuccessful) {

                            Toast.makeText(
                                applicationContext,
                                "Signup Success",
                                Toast.LENGTH_SHORT
                            ).show()

                            startActivity(
                                Intent(
                                    this@SignupActivity,
                                    LoginActivity::class.java
                                )
                            )

                            finish()

                        } else {

                            Toast.makeText(
                                applicationContext,
                                "Signup Failed",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    }

                    override fun onFailure(
                        call: Call<SimpleResponse>,
                        t: Throwable
                    ) {

                        Toast.makeText(
                            applicationContext,
                            "Error: ${t.message}",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                })
        }

        // ✅ Login text click
        loginText.setOnClickListener {

            startActivity(
                Intent(
                    this@SignupActivity,
                    LoginActivity::class.java
                )
            )
        }
    }
}