package com.simats.brainbattle

import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.widget.*
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import com.simats.brainbattle.api.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class LogicLevelsActivity : AppCompatActivity() {

    private val totalLevels = 100

    private lateinit var gridLayout: GridLayout
    private lateinit var progressBar: ProgressBar
    private lateinit var progressText: TextView
    private lateinit var backBtn: ImageView

    private var progressList = listOf<ProgressItem>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_logic_levels)

        gridLayout = findViewById(R.id.levelsGrid)
        progressBar = findViewById(R.id.progressBar)
        progressText = findViewById(R.id.progressText)
        backBtn = findViewById(R.id.back)

        // ✅ BACK BUTTON CLICK
        backBtn.setOnClickListener {

            val intent = Intent(
                this,
                HomeActivity::class.java
            )

            startActivity(intent)
            finish()
        }

        // ✅ PHONE BACK BUTTON (NEW WAY)
        onBackPressedDispatcher.addCallback(
            this,
            object : OnBackPressedCallback(true) {

                override fun handleOnBackPressed() {

                    val intent = Intent(
                        this@LogicLevelsActivity,
                        HomeActivity::class.java
                    )

                    startActivity(intent)
                    finish()
                }
            })

        loadProgress()
    }

    // ✅ refresh after game
    override fun onResume() {
        super.onResume()
        loadProgress()
    }

    // ✅ LOAD FROM BACKEND
    private fun loadProgress() {

        val prefs =
            getSharedPreferences(
                "BrainBattlePrefs",
                Context.MODE_PRIVATE
            )

        val email =
            prefs.getString("email", "") ?: ""

        ApiClient.instance
            .getProgress(email, "logic")
            .enqueue(object :
                Callback<List<ProgressItem>> {

                override fun onResponse(
                    call: Call<List<ProgressItem>>,
                    response: Response<List<ProgressItem>>
                ) {

                    progressList =
                        response.body() ?: listOf()

                    generateLevels()
                }

                override fun onFailure(
                    call: Call<List<ProgressItem>>,
                    t: Throwable
                ) {

                    progressList = listOf()
                    generateLevels()
                }
            })
    }

    // ✅ CREATE LEVEL GRID
    private fun generateLevels() {

        gridLayout.removeAllViews()

        var lastCompleted = 0

        for (p in progressList) {

            if (p.level > lastCompleted) {
                lastCompleted = p.level
            }
        }

        progressBar.max = totalLevels
        progressBar.progress = lastCompleted

        progressText.text =
            "$lastCompleted / $totalLevels Levels"

        for (i in 1..totalLevels) {

            val card = LinearLayout(this)

            val params =
                GridLayout.LayoutParams()

            params.width = 0
            params.height = dpToPx(90)

            params.columnSpec =
                GridLayout.spec(
                    GridLayout.UNDEFINED,
                    1f
                )

            params.setMargins(
                14, 14, 14, 14
            )

            card.layoutParams = params
            card.orientation =
                LinearLayout.VERTICAL

            card.gravity = Gravity.CENTER
            card.setPadding(8, 8, 8, 8)

            val levelNumber =
                TextView(this)

            levelNumber.text = i.toString()
            levelNumber.textSize = 18f
            levelNumber.gravity = Gravity.CENTER
            levelNumber.setTextColor(Color.BLACK)

            val stars =
                TextView(this)

            stars.gravity = Gravity.CENTER

            val progress =
                progressList.find {
                    it.level == i
                }

            // ✅ COMPLETED
            if (progress != null) {

                card.setBackgroundResource(
                    R.drawable.card_bg
                )

                stars.text =
                    "★".repeat(
                        progress.stars
                    )

                stars.setTextColor(
                    Color.parseColor(
                        "#FFC107"
                    )
                )
            }

            // ✅ NEXT LEVEL
            else if (
                i == lastCompleted + 1
                || lastCompleted == 0 && i == 1
            ) {

                card.setBackgroundResource(
                    R.drawable.button_gradient
                )

                levelNumber.setTextColor(
                    Color.WHITE
                )

                stars.text = "★"

                stars.setTextColor(
                    Color.WHITE
                )
            }

            // ✅ LOCKED
            else {

                card.setBackgroundResource(
                    R.drawable.lock_levels
                )

                val lock =
                    ImageView(this)

                lock.setImageResource(
                    R.drawable.ic_lock
                )

                lock.alpha = 0.4f

                card.addView(lock)

                gridLayout.addView(card)

                continue
            }

            card.addView(levelNumber)
            card.addView(stars)

            // 🎮 OPEN LOGIC GAME
            card.setOnClickListener {

                val intent =
                    Intent(
                        this,
                        LogicGameActivity::class.java
                    )

                intent.putExtra(
                    "LEVEL",
                    i
                )

                startActivity(intent)
            }

            gridLayout.addView(card)
        }
    }

    private fun dpToPx(
        dp: Int
    ): Int {

        return (
                dp *
                        resources.displayMetrics.density
                ).toInt()
    }
}