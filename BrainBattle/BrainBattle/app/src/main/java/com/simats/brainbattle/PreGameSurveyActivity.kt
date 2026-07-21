package com.simats.brainbattle

import android.os.Bundle
import android.view.View
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton

class PreGameSurveyActivity : AppCompatActivity() {

    private lateinit var txtProgress: TextView
    private lateinit var txtQuestion: TextView
    private lateinit var btnNext: MaterialButton

    private lateinit var btnOption1: LinearLayout
    private lateinit var btnOption2: LinearLayout
    private lateinit var btnOption3: LinearLayout
    private lateinit var btnOption4: LinearLayout

    private lateinit var txtOption1Text: TextView
    private lateinit var txtOption2Text: TextView
    private lateinit var txtOption3Text: TextView
    private lateinit var txtOption4Text: TextView

    private lateinit var txtOption1Percent: TextView
    private lateinit var txtOption2Percent: TextView
    private lateinit var txtOption3Percent: TextView
    private lateinit var txtOption4Percent: TextView

    private var currentQuestionIndex = 0
    private var selectedOptionIndex = -1

    private val questions = arrayOf(
        Question(
            "How does your child react when a toy does not work?",
            arrayOf("Wants help immediately", "Tries a few times first", "Keeps trying patiently", "Finds another toy"),
            arrayOf(20, 45, 25, 10)
        ),
        Question(
            "Does your child group similar toys together during play?",
            arrayOf("Not yet", "Sometimes, with guidance", "Often does it independently", "Always groups them"),
            arrayOf(15, 40, 35, 10)
        ),
        Question(
            "How often does your child ask questions about new things?",
            arrayOf("Rarely asks questions", "Asks questions occasionally", "Asks many questions daily", "Constantly explores everything"),
            arrayOf(10, 30, 45, 15)
        ),
        Question(
            "Can your child follow a simple two-step instruction?",
            arrayOf("Needs help each time", "Follows it sometimes", "Follows it most times", "Easily follows every time"),
            arrayOf(15, 35, 40, 10)
        ),
        Question(
            "How does your child complete simple matching games or puzzles?",
            arrayOf("Needs a lot of time", "Takes time to figure it out", "Completes them fairly quickly", "Solves them very fast"),
            arrayOf(20, 40, 30, 10)
        )
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_pre_game_survey)

        txtProgress = findViewById(R.id.txtProgress)
        txtQuestion = findViewById(R.id.txtQuestion)
        btnNext = findViewById(R.id.btnNext)

        btnOption1 = findViewById(R.id.btnOption1)
        btnOption2 = findViewById(R.id.btnOption2)
        btnOption3 = findViewById(R.id.btnOption3)
        btnOption4 = findViewById(R.id.btnOption4)

        txtOption1Text = findViewById(R.id.txtOption1Text)
        txtOption2Text = findViewById(R.id.txtOption2Text)
        txtOption3Text = findViewById(R.id.txtOption3Text)
        txtOption4Text = findViewById(R.id.txtOption4Text)

        txtOption1Percent = findViewById(R.id.txtOption1Percent)
        txtOption2Percent = findViewById(R.id.txtOption2Percent)
        txtOption3Percent = findViewById(R.id.txtOption3Percent)
        txtOption4Percent = findViewById(R.id.txtOption4Percent)

        setupQuestion()

        val optionsLayouts = arrayOf(btnOption1, btnOption2, btnOption3, btnOption4)
        for (i in optionsLayouts.indices) {
            optionsLayouts[i].setOnClickListener {
                if (selectedOptionIndex == -1) {
                    selectOption(i)
                }
            }
        }

        btnNext.setOnClickListener {
            if (currentQuestionIndex < questions.size - 1) {
                currentQuestionIndex++
                selectedOptionIndex = -1
                setupQuestion()
            } else {
                Toast.makeText(this, "Thank you for completing the survey!", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }

    private fun setupQuestion() {
        val q = questions[currentQuestionIndex]
        txtProgress.text = "Question ${currentQuestionIndex + 1} of ${questions.size}"
        txtQuestion.text = q.text

        txtOption1Text.text = q.options[0]
        txtOption2Text.text = q.options[1]
        txtOption3Text.text = q.options[2]
        txtOption4Text.text = q.options[3]

        txtOption1Percent.text = "${q.percentages[0]}%"
        txtOption2Percent.text = "${q.percentages[1]}%"
        txtOption3Percent.text = "${q.percentages[2]}%"
        txtOption4Percent.text = "${q.percentages[3]}%"

        txtOption1Percent.visibility = View.GONE
        txtOption2Percent.visibility = View.GONE
        txtOption3Percent.visibility = View.GONE
        txtOption4Percent.visibility = View.GONE

        btnOption1.setBackgroundResource(R.drawable.card_bg)
        btnOption2.setBackgroundResource(R.drawable.card_bg)
        btnOption3.setBackgroundResource(R.drawable.card_bg)
        btnOption4.setBackgroundResource(R.drawable.card_bg)

        btnNext.isEnabled = false
    }

    private fun selectOption(index: Int) {
        selectedOptionIndex = index

        txtOption1Percent.visibility = View.VISIBLE
        txtOption2Percent.visibility = View.VISIBLE
        txtOption3Percent.visibility = View.VISIBLE
        txtOption4Percent.visibility = View.VISIBLE

        val optionsLayouts = arrayOf(btnOption1, btnOption2, btnOption3, btnOption4)
        for (i in optionsLayouts.indices) {
            if (i == index) {
                optionsLayouts[i].setBackgroundResource(R.drawable.button_gradient)
            }
        }

        btnNext.isEnabled = true
    }

    data class Question(
        val text: String,
        val options: Array<String>,
        val percentages: Array<Int>
    )
}
