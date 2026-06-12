package com.simats.brainbattle

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity

class ProfileActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_profile)

        val logout = findViewById<Button>(R.id.btnLogout)

        logout.setOnClickListener {

            val prefs = getSharedPreferences("BrainBattlePrefs", Context.MODE_PRIVATE)
            prefs.edit().clear().apply()

            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }
    }
}