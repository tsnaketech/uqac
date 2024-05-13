package stev.kwikemart;

public abstract class ItemException extends StoreException {
   private static final long serialVersionUID = 1L;

   public ItemException(String upc, String message) {
      super("Exception for item " + upc + ": " + message);
   }
}
