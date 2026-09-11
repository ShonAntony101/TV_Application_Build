package com.example.firecatalog

import android.graphics.Color
import android.view.ViewGroup
import androidx.leanback.widget.ImageCardView
import androidx.leanback.widget.Presenter
import com.bumptech.glide.Glide
import com.example.firecatalog.model.CatalogItem

private const val CARD_WIDTH = 300
private const val CARD_HEIGHT = 170

/**
 * Tells Leanback's row/grid views how to draw a single [CatalogItem] as a card.
 */
class CardPresenter : Presenter() {

    override fun onCreateViewHolder(parent: ViewGroup): ViewHolder {
        val cardView = ImageCardView(parent.context).apply {
            isFocusable = true
            isFocusableInTouchMode = true
            setMainImageDimensions(CARD_WIDTH, CARD_HEIGHT)
        }
        return ViewHolder(cardView)
    }

    override fun onBindViewHolder(viewHolder: ViewHolder, item: Any) {
        val catalogItem = item as CatalogItem
        val cardView = viewHolder.view as ImageCardView

        cardView.titleText = catalogItem.title
        cardView.contentText = catalogItem.category
        cardView.setMainImageDimensions(CARD_WIDTH, CARD_HEIGHT)

        Glide.with(cardView.context)
            .load(catalogItem.imageUrl)
            .centerCrop()
            .into(cardView.mainImageView)

        cardView.setInfoAreaBackgroundColor(Color.parseColor("#212121"))
    }

    override fun onUnbindViewHolder(viewHolder: ViewHolder) {
        val cardView = viewHolder.view as ImageCardView
        Glide.with(cardView.context).clear(cardView.mainImageView)
        cardView.mainImage = null
    }
}
