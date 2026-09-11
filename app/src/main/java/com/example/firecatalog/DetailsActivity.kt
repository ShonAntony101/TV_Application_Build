package com.example.firecatalog

import android.os.Build
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import com.example.firecatalog.model.CatalogItem

/**
 * Details screen: shown after selecting an item on the home/catalog grid.
 * Kept as a plain Activity with standard Views (rather than Leanback's
 * DetailsSupportFragment) so it's easy to read and customize.
 */
class DetailsActivity : AppCompatActivity() {

    companion object {
        const val EXTRA_ITEM = "extra_catalog_item"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_details)

        val item = getCatalogItemExtra() ?: run {
            finish()
            return
        }

        val image = findViewById<ImageView>(R.id.details_image)
        val category = findViewById<TextView>(R.id.details_category)
        val title = findViewById<TextView>(R.id.details_title)
        val description = findViewById<TextView>(R.id.details_description)
        val backButton = findViewById<Button>(R.id.details_back_button)

        category.text = item.category
        title.text = item.title
        description.text = item.description

        Glide.with(this)
            .load(item.imageUrl)
            .centerCrop()
            .into(image)

        backButton.setOnClickListener { finish() }
        backButton.requestFocus()
    }

    @Suppress("DEPRECATION")
    private fun getCatalogItemExtra(): CatalogItem? {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            intent.getSerializableExtra(EXTRA_ITEM, CatalogItem::class.java)
        } else {
            intent.getSerializableExtra(EXTRA_ITEM) as? CatalogItem
        }
    }
}
