package com.simats.brainbattle

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.simats.brainbattle.api.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ForgotPasswordActivity : AppCompatActivity() {

    private lateinit var emailEditText: EditText
    private lateinit var resetButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_forgot_password)

        emailEditText = findViewById(R.id.emailEditText)
        resetButton = findViewById(R.id.resetButton)

        resetButton.setOnClickListener {

            val email = emailEditText.text.toString().trim()

            if (email.isEmpty()) {
                Toast.makeText(this, "Enter email", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            ApiClient.instance.forgotPassword(UserRequest(email))
                .enqueue(object : Callback<MessageResponse> {

                    override fun onResponse(
                        call: Call<MessageResponse>,
                        response: Response<MessageResponse>
                    ) {

                        if (response.isSuccessful && response.body() != null) {

                            val res = response.body()!!

                            if (res.status == "success") {

                                Toast.makeText(
                                    this@ForgotPasswordActivity,
                                    res.message,
                                    Toast.LENGTH_SHORT
                                ).show()

                                // ✅ Move to Change Password
                                startActivity(
                                    Intent(
                                        this@ForgotPasswordActivity,
                                        ChangePasswordActivity::class.java
                                    ).putExtra("email", email)
                                )

                            } else {
                                Toast.makeText(
                                    this@ForgotPasswordActivity,
                                    res.message,
                                    Toast.LENGTH_SHORT
                                ).show()
                            }

                        } else {
                            Toast.makeText(
                                this@ForgotPasswordActivity,
                                "Server error",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    }

                    override fun onFailure(
                        call: Call<MessageResponse>,
                        t: Throwable
                    ) {
                        Toast.makeText(
                            this@ForgotPasswordActivity,
                            "Network error: ${t.message}",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                })
        }
    }
}