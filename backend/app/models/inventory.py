"""Inventory management models."""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel


class Equipment(BaseModel):
    """Equipment/Asset model."""
    __tablename__ = "equipment"

    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=True)
    category = Column(String(100), nullable=False)  # strength, cardio, accessories
    quantity = Column(Integer, default=1)
    purchase_date = Column(DateTime, nullable=False)
    purchase_price = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)
    warranty_expiry = Column(DateTime, nullable=True)
    last_maintenance = Column(DateTime, nullable=True)
    next_maintenance = Column(DateTime, nullable=True)
    location = Column(String(255), nullable=True)  # Zone/Area in gym
    condition = Column(String(50), default="good")  # good, fair, poor, maintenance_needed
    notes = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    branch = relationship("Branch", back_populates="equipment")
    maintenance_logs = relationship("EquipmentMaintenance", back_populates="equipment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Equipment(id={self.id}, name={self.name}, branch_id={self.branch_id})>"


class EquipmentMaintenance(BaseModel):
    """Equipment maintenance log."""
    __tablename__ = "equipment_maintenance"

    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False, index=True)
    maintenance_date = Column(DateTime, nullable=False)
    maintenance_type = Column(String(100), nullable=False)  # preventive, corrective, repair
    description = Column(Text, nullable=True)
    cost = Column(Float, nullable=True)
    performed_by = Column(String(255), nullable=True)
    next_maintenance_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_logs")

    def __repr__(self):
        return f"<EquipmentMaintenance(equipment_id={self.equipment_id}, date={self.maintenance_date})>"


class InventoryItem(BaseModel):
    """Inventory item model for supplements, merchandise etc."""
    __tablename__ = "inventory_items"

    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=True)
    category = Column(String(100), nullable=False)  # supplement, merchandise, consumable
    quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, default=5)
    unit_cost = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    supplier_id = Column(Integer, nullable=True)
    location = Column(String(255), nullable=True)  # Shelf/Storage location
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    branch = relationship("Branch")
    stock_movements = relationship("StockMovement", back_populates="inventory_item", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InventoryItem(id={self.id}, name={self.name}, quantity={self.quantity})>"


class StockMovement(BaseModel):
    """Stock movement tracking (in/out)."""
    __tablename__ = "stock_movements"

    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False, index=True)
    movement_type = Column(String(50), nullable=False)  # in, out, adjustment, damage
    quantity = Column(Integer, nullable=False)
    movement_date = Column(DateTime, default=datetime.utcnow)
    reason = Column(String(255), nullable=False)
    reference_number = Column(String(100), nullable=True)  # PO, Invoice, etc.
    recorded_by = Column(Integer, nullable=True)  # Staff ID
    notes = Column(Text, nullable=True)
    
    # Relationships
    inventory_item = relationship("InventoryItem", back_populates="stock_movements")

    def __repr__(self):
        return f"<StockMovement(inventory_id={self.inventory_item_id}, type={self.movement_type}, qty={self.quantity})>"
