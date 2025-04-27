// Copyright 2023 The Lynx Authors. All rights reserved.
// Licensed under the Apache License Version 2.0 that can be found in the
// LICENSE file in the root directory of this source tree.

#ifndef CORE_RUNTIME_VM_LEPUS_REF_COUNTED_CLASS_H_
#define CORE_RUNTIME_VM_LEPUS_REF_COUNTED_CLASS_H_

#include <memory>

#include "base/include/fml/memory/ref_counted.h"
#include "core/runtime/vm/lepus/lepus_value.h"
#include "core/runtime/vm/lepus/ref_type.h"

namespace lynx {
namespace lepus {
class RefCountedBase : public fml::RefCountedThreadSafeStorage {
 public:
  void ReleaseSelf() const override { delete this; }
  ~RefCountedBase() override = default;

  virtual bool IsConst() const { return false; }

  /*
   * Return RefType of this RefCountedBase.
   * ByteArray in core/runtime/vm/lepus/byte_array.h,
   * Value_JSOBject in core/runtime/vm/lepus/js_object.h,
   * Element in core/renderer/dom/element.h,
   * AirElement in core/renderer/dom/air/air_element/air_element.h
   */
  virtual RefType GetRefType() const = 0;

 protected:
  RefCountedBase() = default;
};

class RefCounted : public RefCountedBase {
 public:
  std::unique_ptr<Value> js_object_cache;
};

}  // namespace lepus
}  // namespace lynx

#endif  // CORE_RUNTIME_VM_LEPUS_REF_COUNTED_CLASS_H_
