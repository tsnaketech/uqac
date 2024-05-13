package stev.kwikemart;

public final class Item {
   private final String m_upc;
   private final String m_description;
   private final double m_retailPrice;
   private final double m_quantity;

   public Item(String upc, String description, double quantity, double retail_price) {
      this.m_upc = upc;
      this.m_description = description;
      this.m_quantity = quantity;
      this.m_retailPrice = retail_price;
   }

   public final String getUpc() {
      return this.m_upc;
   }

   public final String getDescription() {
      return this.m_description;
   }

   public final double getQuantity() {
      return this.m_quantity;
   }

   public final double getRetailPrice() {
      return this.m_retailPrice;
   }

   public int hashCode() {
      return this.m_upc.hashCode();
   }

   public boolean equals(Object o) {
      if (o != null && o instanceof Item) {
         Item i = (Item)o;
         return i.m_upc.compareToIgnoreCase(this.m_upc) == 0;
      } else {
         return false;
      }
   }
}
