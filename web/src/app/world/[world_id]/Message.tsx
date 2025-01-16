import { useState, useEffect, useRef, forwardRef } from 'react'
import classNames from 'classnames'
import _ from "lodash"

interface MessageProps {
  text: string,
  onIntersectionChange?: (visible: boolean) => void,
  charAspectRatio: number
  intersectionMargin?: string,
  className?: string,
  fit?: boolean,
}

export const Message = forwardRef<HTMLDivElement, MessageProps>(({ text, onIntersectionChange, intersectionMargin, className, fit, charAspectRatio }, ref) => {
  const internalRef = useRef<HTMLDivElement>(null)
  const [fitFontSize, setFitFontSize] = useState<number>()

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        onIntersectionChange && onIntersectionChange(entry.isIntersecting);
      },
      { rootMargin: intersectionMargin }
    );
    if(internalRef.current){
      observer.observe(internalRef.current)
      const frozenRef = internalRef.current
      return () => {
        if(internalRef.current){
          observer.unobserve(frozenRef)
        }
      }
    }
  }, [internalRef.current]);

  useEffect(() => {
    if(fit){
      let lines: string[] = text.split('\n');
      const longestLine = _.max(lines.map(l => l.length)) ?? 0
      setFitFontSize(((internalRef.current?.clientWidth ?? 0) - 30) / longestLine / charAspectRatio)
    }
  })

  return (
    <div
      className={classNames(className)}
      style={fit? {fontSize: fitFontSize, lineHeight: '130%'} : {}}
    >
      <div style={{height: 1}} ref={internalRef}/>
      <div style={{height: 1}} ref={ref}/>
      { text }
    </div>
  )
})
