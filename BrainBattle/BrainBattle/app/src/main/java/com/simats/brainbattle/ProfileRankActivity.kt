package com.simats.brainbattle

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.simats.brainbattle.api.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ProfileRankActivity : AppCompatActivity() {

    private lateinit var username: TextView
    private lateinit var emailText: TextView
    private lateinit var rankText: TextView
    private lateinit var starCount: TextView
    private lateinit var levelsCompleted: TextView
    private lateinit var changePasswordBtn: Button
    private lateinit var backBtn: ImageView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_profile_rank)

        username = findViewById(R.id.username)
        emailText = findViewById(R.id.email)
        rankText = findViewById(R.id.rankText)
        starCount = findViewById(R.id.starCount)
        levelsCompleted = findViewById(R.id.levelsCompleted)
        changePasswordBtn = findViewById(R.id.changePasswordBtn)
        backBtn = findViewById(R.id.backBtn)

        val prefs = getSharedPreferences(
            "BrainBattlePrefs",
            Context.MODE_PRIVATE
        )

        val email = prefs.getString("email", "") ?: ""
        emailText.text = email

        backBtn.setOnClickListener {
            finish()
        }

        // ⭐ OPEN CHANGE PASSWORD SCREEN
        changePasswordBtn.setOnClickListener {

            val intent = Intent(
                this@ProfileRankActivity,
                ChangePasswordActivity::class.java
            )

            intent.putExtra("email", email)

            startActivity(intent)
        }

        loadUser(email)
        loadRank(email)
    }

    private fun loadUser(email: String) {

        ApiClient.instance.getUser(UserRequest(email))
            .enqueue(object : Callback<UserResponse> {

                override fun onResponse(
                    call: Call<UserResponse>,
                    response: Response<UserResponse>
                ) {
                    if (response.isSuccessful) {
                        val user = response.body()
                        username.text = user?.username ?: "User"
                    }
                }

                override fun onFailure(
                    call: Call<UserResponse>,
                    t: Throwable
                ) {
                    Toast.makeText(
                        this@ProfileRankActivity,
                        "Failed to load user",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            })
    }

    private fun loadRank(email: String) {

        ApiClient.instance.getDashboard(email)
            .enqueue(object : Callback<DashboardResponse> {

                override fun onResponse(
                    call: Call<DashboardResponse>,
                    response: Response<DashboardResponse>
                ) {

                    if (response.isSuccessful) {

                        val data = response.body()

                        starCount.text =
                            (data?.total_stars ?: 0).toString()

                        levelsCompleted.text =
                            (data?.levels_completed ?: 0).toString()

                        rankText.text =
                            "#${data?.rank ?: 0}"
                    }
                }

                override fun onFailure(
                    call: Call<DashboardResponse>,
                    t: Throwable
                ) {
                    Toast.makeText(
                        this@ProfileRankActivity,
                        "Failed to load rank data",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            })
    }
}