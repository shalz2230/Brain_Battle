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

class HomeActivity : AppCompatActivity() {

    private lateinit var txtUsername: TextView
    private lateinit var progressLevel: TextView
    private lateinit var scoreText: TextView
    private lateinit var btnStart: Button

    private lateinit var memory: LinearLayout
    private lateinit var logic: LinearLayout
    private lateinit var focus: LinearLayout
    private lateinit var speed: LinearLayout

    private lateinit var levelContainer: LinearLayout
    private lateinit var profileIcon: ImageView

    private var currentLevel = 1
    private var lastGame = "memory"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_homescreen)

        // UI
        txtUsername = findViewById(R.id.txtUsername)
        progressLevel = findViewById(R.id.progressLevel)
        scoreText = findViewById(R.id.scoreText)
        btnStart = findViewById(R.id.btnStart)

        memory = findViewById(R.id.memory_card)
        logic = findViewById(R.id.logic_card)
        focus = findViewById(R.id.focus_card)
        speed = findViewById(R.id.speed_card)

        levelContainer = findViewById(R.id.levelContainer)
        profileIcon = findViewById(R.id.profileIcon)

        // PROFILE CLICK
        profileIcon.setOnClickListener {
            startActivity(Intent(this, ProfileRankActivity::class.java))
        }

        // GET EMAIL
        val prefs = getSharedPreferences("BrainBattlePrefs", Context.MODE_PRIVATE)
        val email = prefs.getString("email", "") ?: ""

        if (email.isEmpty()) {
            Toast.makeText(this, "Login again", Toast.LENGTH_SHORT).show()
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
            return
        }

        // FETCH USERNAME
        ApiClient.instance.getUser(UserRequest(email))
            .enqueue(object : Callback<UserResponse> {
                override fun onResponse(
                    call: Call<UserResponse>,
                    response: Response<UserResponse>
                ) {
                    if (response.isSuccessful) {
                        val username = response.body()?.username
                        txtUsername.text = "Welcome back $username 👋"
                    }
                }

                override fun onFailure(call: Call<UserResponse>, t: Throwable) {
                    Toast.makeText(applicationContext, t.message, Toast.LENGTH_SHORT).show()
                }
            })

        // FETCH DASHBOARD
        ApiClient.instance.getDashboard(email)
            .enqueue(object : Callback<DashboardResponse> {

                override fun onResponse(
                    call: Call<DashboardResponse>,
                    response: Response<DashboardResponse>
                ) {
                    if (response.isSuccessful) {

                        val data = response.body()

                        currentLevel = data?.current_level ?: 1
                        lastGame = data?.last_game ?: "memory"

                        progressLevel.text =
                            "${lastGame.replaceFirstChar { it.uppercase() }} Level $currentLevel"

                        scoreText.text =
                            "Score: ${data?.total_stars ?: 0} ⭐"

                        showNextLevels(currentLevel)
                    }
                }

                override fun onFailure(call: Call<DashboardResponse>, t: Throwable) {}
            })

        // START BUTTON
        btnStart.setOnClickListener {
            openGame(lastGame, currentLevel)
        }

        // GAME CARDS
        memory.setOnClickListener {
            startActivity(Intent(this, MemoryLevelsActivity::class.java))
        }

        logic.setOnClickListener {
            startActivity(Intent(this, LogicLevelsActivity::class.java))
        }

        focus.setOnClickListener {
            startActivity(Intent(this, FocusLevelsActivity::class.java))
        }

        speed.setOnClickListener {
            startActivity(Intent(this, SpeedLevelsActivity::class.java))
        }
    }

    // SHOW NEXT 4 LEVELS
    private fun showNextLevels(current: Int) {

        levelContainer.removeAllViews()

        val start = current + 1
        val end = current + 4

        for (i in start..end) {

            val view = layoutInflater.inflate(
                R.layout.level_item,
                levelContainer,
                false
            )

            val txtLevel = view.findViewById<TextView>(R.id.txtLevelNumber)
            val txtType = view.findViewById<TextView>(R.id.txtLevelType)

            txtLevel.text = i.toString()

            txtType.text = when {
                i <= 5 -> "Easy"
                i <= 10 -> "Medium"
                else -> "Hard"
            }

            view.setOnClickListener {
                openGame(lastGame, i)
            }

            levelContainer.addView(view)
        }
    }

    // OPEN GAME
    private fun openGame(game: String, level: Int) {

        val intent = when (game) {
            "memory" -> Intent(this, MemoryLevelsActivity::class.java)
            "logic" -> Intent(this, LogicLevelsActivity::class.java)
            "focus" -> Intent(this, FocusLevelsActivity::class.java)
            else -> Intent(this, SpeedLevelsActivity::class.java)
        }

        intent.putExtra("LEVEL", level)
        startActivity(intent)
    }
}