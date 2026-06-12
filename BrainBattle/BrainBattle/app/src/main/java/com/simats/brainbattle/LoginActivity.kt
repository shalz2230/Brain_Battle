package com.simats.brainbattle

import android.content.Intent
import android.content.Context
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

class LoginActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val email = findViewById<EditText>(R.id.emailEditText)
        val password = findViewById<EditText>(R.id.passwordEditText)

        val loginBtn = findViewById<MaterialButton>(R.id.loginButton)
        val signupText = findViewById<TextView>(R.id.signupText)
        val forgotText = findViewById<TextView>(R.id.forgotText)

        loginBtn.setOnClickListener {

            val emailText = email.text.toString().trim()
            val passwordText = password.text.toString().trim()

            if (emailText.isEmpty() || passwordText.isEmpty()) {
                Toast.makeText(
                    this,
                    "Enter email & password",
                    Toast.LENGTH_SHORT
                ).show()
                return@setOnClickListener
            }

            val request = AuthRequest(
                email = emailText,
                password = passwordText
            )

            ApiClient.instance.login(request)
                .enqueue(object : Callback<LoginResponse> {

                    override fun onResponse(
                        call: Call<LoginResponse>,
                        response: Response<LoginResponse>
                    ) {

                        if (response.isSuccessful && response.body() != null) {

                            val user = response.body()!!

                            val prefs = getSharedPreferences(
                                "BrainBattlePrefs",
                                Context.MODE_PRIVATE
                            )

                            prefs.edit()
                                .putString("email", user.email)
                                .apply()

                            Toast.makeText(
                                applicationContext,
                                "Welcome ${user.username}",
                                Toast.LENGTH_SHORT
                            ).show()

                            val intent = Intent(
                                this@LoginActivity,
                                HomeActivity::class.java
                            )

                            startActivity(intent)
                            finish()

                        } else {

                            Toast.makeText(
                                applicationContext,
                                "Login Failed",
                                Toast.LENGTH_SHORT
                            ).show()

                        }
                    }

                    override fun onFailure(
                        call: Call<LoginResponse>,
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

        signupText.setOnClickListener {

            startActivity(
                Intent(
                    this@LoginActivity,
                    SignupActivity::class.java
                )
            )
        }

        // ⭐ OPEN FORGOT PASSWORD SCREEN
        forgotText.setOnClickListener {

            startActivity(
                Intent(
                    this@LoginActivity,
                    ForgotPasswordActivity::class.java
                )
            )
        }
    }
}