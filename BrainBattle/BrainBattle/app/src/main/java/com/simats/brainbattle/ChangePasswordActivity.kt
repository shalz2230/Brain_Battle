package com.simats.brainbattle

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.simats.brainbattle.api.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ChangePasswordActivity : AppCompatActivity() {

    private lateinit var emailEditText: EditText
    private lateinit var passwordEditText: EditText
    private lateinit var changeButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_change_password)

        emailEditText = findViewById(R.id.emailEditText)
        passwordEditText = findViewById(R.id.passwordEditText)
        changeButton = findViewById(R.id.changeButton)

        // ✅ Get email safely
        val email = intent.getStringExtra("email") ?: ""
        emailEditText.setText(email)

        changeButton.setOnClickListener {

            val newPassword = passwordEditText.text.toString().trim()

            if (email.isEmpty() || newPassword.isEmpty()) {
                Toast.makeText(this, "All fields required", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            ApiClient.instance.changePassword(
                ChangePasswordRequest(email, newPassword)
            ).enqueue(object : Callback<MessageResponse> {

                override fun onResponse(
                    call: Call<MessageResponse>,
                    response: Response<MessageResponse>
                ) {

                    if (response.isSuccessful && response.body() != null) {

                        val res = response.body()!!

                        if (res.status == "success") {

                            Toast.makeText(
                                this@ChangePasswordActivity,
                                res.message,
                                Toast.LENGTH_LONG
                            ).show()

                            finish()

                        } else {
                            Toast.makeText(
                                this@ChangePasswordActivity,
                                res.message,
                                Toast.LENGTH_SHORT
                            ).show()
                        }

                    } else {
                        Toast.makeText(
                            this@ChangePasswordActivity,
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
                        this@ChangePasswordActivity,
                        "Network error: ${t.message}",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            })
        }
    }
}