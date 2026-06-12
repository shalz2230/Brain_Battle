package com.simats.brainbattle

import android.content.Intent
import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton
import com.simats.brainbattle.api.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ResultActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_result)

        val txtLevel = findViewById<TextView>(R.id.txtLevel)
        val txtStars = findViewById<TextView>(R.id.txtStars)
        val txtTime = findViewById<TextView>(R.id.txtTime)
        val btnContinue = findViewById<MaterialButton>(R.id.btnContinue)

        // ✅ Get data
        val level = intent.getIntExtra("LEVEL", 1)
        val stars = intent.getIntExtra("STARS", 1)
        val time = intent.getIntExtra("TIME", 0)

        // ✅ NEW (get game type)
        val type =
            intent.getStringExtra("TYPE")
                ?: "memory"

        txtLevel.text =
            "Level $level Completed 🎉"

        txtStars.text =
            "★".repeat(stars)

        txtTime.text =
            "Time: ${time}s"

        // ✅ Save progress
        saveProgress(
            type,
            level,
            stars,
            time
        )

        // ✅ Continue button
        btnContinue.setOnClickListener {

            val intent = when (type) {

                "logic" -> Intent(
                    this,
                    LogicLevelsActivity::class.java
                )

                "focus" -> Intent(
                    this,
                    FocusLevelsActivity::class.java
                )

                "speed" -> Intent(
                    this,
                    SpeedLevelsActivity::class.java
                )

                else -> Intent(
                    this,
                    MemoryLevelsActivity::class.java
                )
            }

            intent.flags =
                Intent.FLAG_ACTIVITY_CLEAR_TOP

            startActivity(intent)
            finish()
        }
    }

    // ✅ SAVE TO BACKEND
    private fun saveProgress(
        type: String,
        level: Int,
        stars: Int,
        time: Int
    ) {

        val prefs =
            getSharedPreferences(
                "BrainBattlePrefs",
                MODE_PRIVATE
            )

        val email =
            prefs.getString("email", "")
                ?: ""

        val req =
            ProgressRequest(
                email,
                type,   // ✅ dynamic
                level,
                stars,
                time
            )

        ApiClient.instance
            .saveProgress(req)
            .enqueue(
                object :
                    Callback<SimpleResponse> {

                    override fun onResponse(
                        call: Call<SimpleResponse>,
                        response: Response<SimpleResponse>
                    ) {
                    }

                    override fun onFailure(
                        call: Call<SimpleResponse>,
                        t: Throwable
                    ) {
                    }
                })
    }
}